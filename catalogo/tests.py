from decimal import Decimal

from django.contrib import admin
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import ConsultaCliente, Producto
from .views import STOCK_CRITICO_UMBRAL


class CatalogoCrudTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username='gestor',
            password='test-password',
            is_staff=True,
        )
        self.client.force_login(self.staff)
        self.producto = Producto.objects.create(
            nombre='Martillo',
            categoria='Herramientas',
            precio='12.50',
            stock=5,
        )

    def test_staff_can_create_product_and_returns_to_database_listing(self):
        response = self.client.post(reverse('catalogo:crear_producto'), {
            'nombre': 'Taladro',
            'categoria': 'Herramientas',
            'precio': '89.90',
            'stock': '3',
        }, follow=True)

        self.assertEqual(response.redirect_chain[-1][0], reverse('catalogo:lista'))
        self.assertTrue(Producto.objects.filter(nombre='Taladro', stock=3).exists())
        self.assertContains(response, 'Taladro')
        self.assertContains(response, 'Se creó el producto')

    def test_invalid_product_is_not_saved_and_displays_errors(self):
        response = self.client.post(reverse('catalogo:crear_producto'), {
            'nombre': 'Producto inválido',
            'categoria': 'Herramientas',
            'precio': '0',
            'stock': '-1',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertContains(response, 'El valor debe ser mayor o igual a 0.01.', status_code=400)

    def test_staff_can_edit_product_and_returns_to_listing(self):
        response = self.client.post(
            reverse('catalogo:editar_producto', args=[self.producto.pk]),
            {
                'nombre': 'Martillo reforzado',
                'categoria': 'Herramientas',
                'precio': '15.00',
                'stock': '8',
            },
            follow=True,
        )

        self.producto.refresh_from_db()
        self.assertEqual(response.redirect_chain[-1][0], reverse('catalogo:lista'))
        self.assertEqual(self.producto.nombre, 'Martillo reforzado')
        self.assertEqual(self.producto.stock, 8)
        self.assertContains(response, 'Martillo reforzado')

    def test_staff_can_delete_product_with_post_and_returns_to_listing(self):
        response = self.client.post(
            reverse('catalogo:eliminar_producto', args=[self.producto.pk]),
            follow=True,
        )

        self.assertEqual(response.redirect_chain[-1][0], reverse('catalogo:lista'))
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())
        self.assertContains(response, 'No hay productos disponibles.')
        self.assertContains(response, 'Se eliminó el producto')

    def test_catalog_lists_management_actions_for_staff(self):
        response = self.client.get(reverse('catalogo:lista'))

        self.assertContains(response, reverse('catalogo:editar_producto', args=[self.producto.pk]))
        self.assertContains(response, '¿Eliminar el producto Martillo?')

    def test_anonymous_users_cannot_create_products(self):
        self.client.logout()

        response = self.client.post(reverse('catalogo:crear_producto'), {
            'nombre': 'No autorizado',
            'categoria': 'Herramientas',
            'precio': '1.00',
            'stock': '1',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Producto.objects.count(), 1)


class CatalogoReportesTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Martillo',
            categoria='Herramientas',
            precio='12.50',
            stock=5,
        )

    def test_category_report_uses_database_aggregates(self):
        Producto.objects.create(
            nombre='Alicate',
            categoria='Herramientas',
            precio='20.00',
            stock=0,
        )
        Producto.objects.create(
            nombre='Cable',
            categoria='Electricidad',
            precio='8.00',
            stock=9,
        )

        response = self.client.get(reverse('catalogo:reporte_categorias'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['categorias']),
            [
                {
                    'categoria': 'Electricidad',
                    'cantidad_registros': 1,
                    'promedio_precio': Decimal('8'),
                    'total_stock': 9,
                },
                {
                    'categoria': 'Herramientas',
                    'cantidad_registros': 2,
                    'promedio_precio': Decimal('16.25'),
                    'total_stock': 5,
                },
            ],
        )
        self.assertContains(response, 'Cantidad de productos')
        self.assertContains(response, '$16.25')

    def test_critical_stock_report_filters_and_orders_database_records(self):
        Producto.objects.create(
            nombre='Nivel',
            categoria='Herramientas',
            precio='10.00',
            stock=STOCK_CRITICO_UMBRAL,
        )
        Producto.objects.create(
            nombre='Alicate',
            categoria='Herramientas',
            precio='5.00',
            stock=0,
        )
        Producto.objects.create(
            nombre='Taladro',
            categoria='Herramientas',
            precio='80.00',
            stock=STOCK_CRITICO_UMBRAL + 1,
        )

        response = self.client.get(reverse('catalogo:reporte_stock_critico'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context['productos']),
            [
                Producto.objects.get(nombre='Alicate'),
                self.producto,
                Producto.objects.get(nombre='Nivel'),
            ],
        )
        self.assertNotContains(response, 'Taladro')
        self.assertContains(response, f'{STOCK_CRITICO_UMBRAL} unidades o menos')

    def test_base_navigation_links_to_both_reports(self):
        response = self.client.get(reverse('catalogo:lista'))

        self.assertContains(response, reverse('catalogo:reporte_categorias'))
        self.assertContains(response, reverse('catalogo:reporte_stock_critico'))


class ConsultaClienteTests(TestCase):
    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Martillo',
            categoria='Herramientas',
            precio='12.50',
            stock=5,
        )

    def test_customer_inquiries_are_registered_in_admin(self):
        self.assertTrue(admin.site.is_registered(ConsultaCliente))

    def test_valid_contact_submission_is_saved_and_confirmed(self):
        response = self.client.post(reverse('catalogo:consulta_cliente'), {
            'nombre': 'Ana Pérez',
            'correo': 'ana@example.com',
            'mensaje': 'Quiero saber más sobre este producto.',
            'producto_interes': str(self.producto.pk),
        })

        self.assertEqual(response.status_code, 200)
        consulta = ConsultaCliente.objects.get()
        self.assertEqual(consulta.nombre, 'Ana Pérez')
        self.assertEqual(consulta.producto_interes, self.producto)
        self.assertIsNotNone(consulta.fecha)
        self.assertContains(response, 'Gracias, Ana Pérez.')

    def test_invalid_email_and_short_required_fields_are_rejected(self):
        response = self.client.post(reverse('catalogo:consulta_cliente'), {
            'nombre': 'A',
            'correo': 'no-es-un-correo',
            'mensaje': 'corto',
            'producto_interes': '',
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ConsultaCliente.objects.count(), 0)
        self.assertContains(response, 'El nombre debe tener al menos 2 caracteres.', status_code=400)
        self.assertContains(response, 'Ingresa un correo electrónico válido.', status_code=400)
        self.assertContains(response, 'El mensaje debe tener al menos 10 caracteres.', status_code=400)

    def test_required_contact_fields_cannot_be_empty(self):
        response = self.client.post(reverse('catalogo:consulta_cliente'), {})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ConsultaCliente.objects.count(), 0)
        self.assertContains(response, 'Ingresa tu nombre.', status_code=400)
        self.assertContains(response, 'Ingresa tu correo electrónico.', status_code=400)
        self.assertContains(response, 'Escribe tu mensaje.', status_code=400)

    def test_contact_submission_requires_csrf_token(self):
        csrf_client = self.client_class(enforce_csrf_checks=True)
        response = csrf_client.post(reverse('catalogo:consulta_cliente'), {
            'nombre': 'Ana Pérez',
            'correo': 'ana@example.com',
            'mensaje': 'Quiero saber más sobre este producto.',
            'producto_interes': '',
        })

        self.assertEqual(response.status_code, 403)
        self.assertEqual(ConsultaCliente.objects.count(), 0)

    def test_contact_form_accepts_valid_csrf_token(self):
        csrf_client = self.client_class(enforce_csrf_checks=True)
        form_response = csrf_client.get(reverse('catalogo:consulta_cliente'))
        csrf_token = csrf_client.cookies['csrftoken'].value

        response = csrf_client.post(reverse('catalogo:consulta_cliente'), {
            'csrfmiddlewaretoken': csrf_token,
            'nombre': 'Ana Pérez',
            'correo': 'ana@example.com',
            'mensaje': 'Quiero saber más sobre este producto.',
            'producto_interes': '',
        })

        self.assertEqual(form_response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ConsultaCliente.objects.count(), 1)

    def test_contact_form_can_be_prefilled_with_product_from_detail_link(self):
        response = self.client.get(
            reverse('catalogo:consulta_cliente'),
            {'producto': self.producto.pk},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'<option value="{self.producto.pk}" selected>')

    def test_product_detail_tracks_only_the_three_most_recent_products(self):
        productos = [self.producto]
        for nombre in ('Alicate', 'Taladro', 'Nivel'):
            productos.append(Producto.objects.create(
                nombre=nombre,
                categoria='Herramientas',
                precio='10.00',
                stock=2,
            ))

        for producto in productos:
            response = self.client.get(reverse('catalogo:detalle', args=[producto.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.client.session['productos_visitados'],
            [productos[3].pk, productos[2].pk, productos[1].pk],
        )
        self.assertEqual(
            [producto['nombre'] for producto in response.context['historial_productos']],
            ['Nivel', 'Taladro', 'Alicate'],
        )
