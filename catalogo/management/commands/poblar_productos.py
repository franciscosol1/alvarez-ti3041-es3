import json
from pathlib import Path

from django.core.management.base import BaseCommand

from catalogo.models import Producto
#pobla la base de datos con el json
#la IA creó este comando de gestión para poblar la base de datos con los productos del archivo JSON.
#despues lo puedes ejecutar con el comando: python manage.py poblar_productos
class Command(BaseCommand):
    help = 'Carga los productos del archivo JSON a la base de datos.'

    def handle(self, *args, **options):
        json_path = Path(__file__).resolve().parents[2] / 'data' / 'productos.json'

        with json_path.open(encoding='utf-8') as archivo:
            productos = json.load(archivo)

        creados = 0
        actualizados = 0

        for item in productos:
            producto, created = Producto.objects.update_or_create(
                id=item['id'],
                defaults={
                    'nombre': item['nombre'],
                    'categoria': item['categoria'],
                    'precio': item['precio'],
                    'stock': item['stock'],
                },
            )
            if created:
                creados += 1
            else:
                actualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Productos cargados: {creados} creados, {actualizados} actualizados.'
            )
        )