from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('articulos', views.articulos, name='admin_articulos'),
    path('ventas', views.ventas, name='admin_ventas'),
    path('stock', views.stock, name='admin_stock'),
    path('eliminar', views.eliminar, name='admin_eliminar'),
    path('detalles/<str:codigo>', views.detalles, name='admin_detalles'),
    path('restaurar', views.restaurar, name='admin_restaurar'),
    path('cambiar_imagen', views.cambiar_image, name='admin_cambiar_image'),
    path('modificar', views.modificar, name='admin_modificar')
]