from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'Convoiturage/index.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('success_page')  # Rediriger vers une page de succèss
            else:
                # Gestion de l'échec de connexion (par exemple, afficher un message d'erreur)
                return render(request, 'Convoiturage/login.html', {'form': form, 'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'Convoiturage/login.html', {'form': form})

from django.shortcuts import render

def success_view(request):
    return render(request, 'Convoiturage/success.html')  # Exemple de page de succès, à créer dans le dossier templates

from django.shortcuts import render, redirect
from django.contrib import messages # Pour afficher des messages de succès/erreur
from .forms import  PassagerRegistrationForm

def register_passager(request):
    if request.method == 'POST':
        form = PassagerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte conducteur a été créé avec succès !')
            return redirect('registration_success') # Redirige vers une page de succès
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = PassagerRegistrationForm() # Formulaire vide pour une requête GET

    return render(request, 'Convoiturage/register_conducteur.html', {'form': form})

def registration_success(request):
    return render(request, 'Convoiturage/registration_success.html')


# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Importez votre modèle Utilisateur si vous avez besoin de récupérer des infos spécifiques
# from .models import Utilisateur

@login_required
def home_view(request):
    """
    Vue de la page d'accueil personnalisée après connexion.
    """
    user = request.user # L'utilisateur connecté

    # Vous pouvez ajouter ici la logique pour récupérer d'autres données
    # Exemple: Récupérer les 3 derniers trajets de l'utilisateur s'ils existent
    # recent_trips = Trip.objects.filter(user=user).order_by('-date')[:3]

    context = {
        'user': user,
        'welcome_message': f"Bienvenue, {user.first_name or user.username} !",
        # 'recent_trips': recent_trips, # Ajoutez ceci si vous avez un modèle Trip
    }
    return render(request, 'myapp/home.html', context)