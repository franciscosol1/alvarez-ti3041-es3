from django.urls import path

from . import views


app_name = 'catalogo'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('catalogo/', views.lista_productos, name='lista'),
    path('catalogo/producto/<int:producto_id>/', views.detalle_producto, name='detalle'),
    path('catalogo/producto/<int:producto_id>/comprar/', views.simular_compra, name='compra'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('panel-admin/', views.panel_admin, name='panel_admin'),
    path('panel-admin/crear/', views.crear_producto, name='crear_producto'),
    path('panel-admin/stock/<int:producto_id>/', views.actualizar_stock, name='actualizar_stock'),
]