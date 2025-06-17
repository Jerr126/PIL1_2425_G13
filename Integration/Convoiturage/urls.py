from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login_register/', views.login_register_view, name='login_register'),
    path('login/', views.login_register_view, name='login'), # Pour le traitement du POST de connexion
    path('register/', views.login_register_view, name='register'), # Pour le traitement du POST d'inscription
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
<<<<<<< HEAD
    path('accounts/profile/', views.profile_view, name='profile'),
=======
     path('search-trip/', views.search_trip_view, name='search_trip'), # Nouvelle URL pour la recherche
    path('propose-trip/', views.propose_trip_view, name='propose_trip'),
>>>>>>> 5f9b0a4e994cca308a34160aa0c578405cbe3698
]
