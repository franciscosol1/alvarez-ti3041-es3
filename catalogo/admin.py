from django.contrib import admin

from .models import ConsultaCliente, Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria',)


@admin.register(ConsultaCliente)
class ConsultaClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'producto_interes', 'fecha')
    search_fields = ('nombre', 'correo', 'mensaje')
    list_filter = ('fecha',)
    readonly_fields = ('fecha',)