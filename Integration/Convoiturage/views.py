from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UtilisateurProfileForm # Importez votre formulaire
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout # Pour la connexion/déconnexion
from .forms import ConnexionForm, UserRegistrationForm # Importez les nouveaux formulaires
from django.db.models import Q # Pour des requêtes complexes (OR, AND)
from datetime import datetime, date, timedelta # 'datetime' et 'date' pour la manipulation des dates/heures
from .forms import UtilisateurProfileForm, TrajetSearchForm, ProposeTripForm
from .models import Trajet # Assurez-vous d'importer votre modèle Trajet


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


@login_required
def search_trip_view(request):
    form = TrajetSearchForm(request.GET or None) # Utilise request.GET pour les paramètres d'URL
    results = [] # Pour stocker les trajets trouvés

    if form.is_valid():
        origine = form.cleaned_data.get('origine')
        destination = form.cleaned_data.get('destination')
        date_depart = form.cleaned_data.get('date_depart')
        nombre_places_min = form.cleaned_data.get('nombre_places_min')

        # Requête de base pour les trajets actifs et futurs
        # Filtrer les trajets qui n'ont pas encore eu lieu
        today = date.today()
        now = datetime.now().time()

        queryset = Trajet.objects.filter(
            actif=True,
            date_depart__gte=today, # La date de départ doit être aujourd'hui ou dans le futur
            nombre_places__gte=nombre_places_min # Au moins le nombre de places requis
        )

        # Filtrage par origine et destination (insensible à la casse)
        if origine:
            queryset = queryset.filter(origine__icontains=origine)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)

        # Filtrage par date de départ spécifique
        if date_depart:
            queryset = queryset.filter(date_depart=date_depart)
            # Si la date est aujourd'hui, filtrer aussi par l'heure
            if date_depart == today:
                queryset = queryset.filter(heure_depart__gte=now)
        else:
            # Si pas de date spécifique, trier les trajets à venir par pertinence (plus tôt = plus pertinent)
            queryset = queryset.order_by('date_depart', 'heure_depart')


        # Logique de "matching" et d'ordre :
        # Les trajets "mieux placés" sont ceux qui correspondent le plus précisément
        # et qui partent le plus tôt.

        # 1. Correspondance exacte d'origine/destination :
        # C'est déjà fait par le filter ci-dessus.

        # 2. Proximité géographique (si vous avez des données de localisation) :
        # Ceci est complexe et nécessiterait des champs de latitude/longitude
        # et une bibliothèque comme GeoDjango ou des calculs de distance Haversine.
        # Pour l'instant, on se base sur les chaînes de caractères.
        # Si vous avez des noms de villes/lieux standardisés, cela simplifie.

        # 3. Ordre par date/heure : Les plus proches dans le temps en premier.
        # C'est géré par queryset.order_by('date_depart', 'heure_depart')

        # 4. Ordre par prix (du moins cher au plus cher, ou option de l'utilisateur)
        # Vous pouvez ajouter .order_by('prix_par_place') si c'est un critère.
        # Exemple: queryset = queryset.order_by('prix_par_place', 'date_depart', 'heure_depart')

        # 5. Ordre par nombre de places disponibles (plus de places = plus de choix)
        # Example: .order_by('-nombre_places')

        results = queryset.select_related('conducteur').all() # Optimisation pour récupérer les infos du conducteur

        if not results:
            messages.info(request, "Aucun trajet correspondant à votre recherche n'a été trouvé.")

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'Convoiturage/search_results.html', context)

# @login_required
def propose_trip_view(request):
    """
    Vue pour qu'un conducteur puisse proposer un trajet.
    """
    # Vérifier si l'utilisateur est un conducteur
    if not request.user.is_conducteur:
        messages.warning(request, "Vous devez être enregistré comme conducteur pour proposer un trajet.")
        return redirect('profile') # Rediriger vers la page de profil pour changer de statut

    if request.method == 'POST':
        form = ProposeTripForm(request.POST) # Vous devrez créer ce formulaire
        if form.is_valid():
            trip = form.save(commit=False)
            trip.conducteur = request.user # Assigner le conducteur actuel
            trip.save()
            messages.success(request, "Votre trajet a été proposé avec succès !")
            return redirect('home') # Rediriger vers la page d'accueil ou de gestion des trajets
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ProposeTripForm() # Initialisez un formulaire vide

    context = {'form': form}
    return render(request, 'Convoiturage/propose_trip.html', context)