from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UtilisateurProfileForm # Importez votre formulaire
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout # Pour la connexion/déconnexion
from .forms import ConnexionForm, UserRegistrationForm # Importez les nouveaux formulaires

# Create your views here.

def home(request):
    return render(request, 'Convoiturage/index.html')

# Vue pour la page de connexion et d'inscription

def login_register_view(request):
    login_form = ConnexionForm(request=request) # AuthenticationForm nécessite 'request' pour se_valid
    registration_form = UserRegistrationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = ConnexionForm(request=request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Connexion réussie !')
                    return redirect('profile') # Rediriger vers la page de profil
                else:
                    messages.error(request, 'Identifiants invalides.')
            else:
                messages.error(request, 'Veuillez corriger les erreurs de connexion.')
        elif 'register_submit' in request.POST:
            registration_form = UserRegistrationForm(request.POST, request.FILES) # Ajout de request.FILES pour la photo
            if registration_form.is_valid():
                user = registration_form.save()
                # Optionnel: connecter l'utilisateur immédiatement après l'inscription
                login(request, user)
                messages.success(request, 'Votre compte a été créé avec succès !')
                return redirect('prolfile') # Rediriger vers la page de profil
            else:
                messages.error(request, 'Veuillez corriger les erreurs d\'inscription.')

    context = {
        'login_form': login_form,
        'registration_form': registration_form,
    }
    return render(request, 'Convoiturage/page_inscription.html', context)

# La vue de déconnexion reste la même
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('login_register')






@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UtilisateurProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès !')
            return redirect('profile') # Redirige vers la même page de profil
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = UtilisateurProfileForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'Convoiturage/page_profile.html', context)