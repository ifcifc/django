from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.user_logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
]