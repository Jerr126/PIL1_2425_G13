from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_register_view, name='login_register'),
    path('login/', views.login_register_view, name='login'),
    path('register/', views.login_register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('search-trip/', views.search_trip_view, name='search_trip'),
    path('propose-trip/', views.propose_trip_view, name='propose_trip'),
    path('settings/', views.settings, name='settings'),
    path('annonce/', views.annonce, name='annonce'),
    path('historique/', views.historique, name='historique'),
    path('reserver/<int:trajet_id>/', views.reserver_trajet, name='reserver_trajet')
    
]
