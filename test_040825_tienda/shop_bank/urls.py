from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='fondos'),
    path('transferir', views.transferir, name='transferir'),
]