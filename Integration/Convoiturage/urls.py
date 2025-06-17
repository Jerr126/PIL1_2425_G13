from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login_register/', views.login_register_view, name='login_register'),
    path('login/', views.login_register_view, name='login'), # Pour le traitement du POST de connexion
    path('register/', views.login_register_view, name='register'), # Pour le traitement du POST d'inscription
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
