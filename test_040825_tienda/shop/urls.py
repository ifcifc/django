from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tienda'),
    path('carrito', views.carrito, name='carrito'),
    path('detalles/<str:codigo>', views.detalles, name='detalles'),
    path('comprar', views.buy, name='comprar'),
]