from decimal import Decimal

from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Producto
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
