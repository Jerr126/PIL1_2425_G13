from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success_page'),
    path('register_conducteur/', views.register_passager, name='register_passager'),
    path('register/success/', views.registration_success, name='registration_success'),

]
