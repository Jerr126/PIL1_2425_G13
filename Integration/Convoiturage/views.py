from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UtilisateurProfileForm, UserRegistrationForm, ConnexionForm, ProposeTripForm, TrajetSearchForm
from django.contrib.auth import authenticate, login, logout # Pour la connexion/déconnexion
from django.db.models import Q # Pour des requêtes complexes (OR, AND)
from datetime import datetime, date # 'datetime' et 'date' pour la manipulation des dates/heures 
from .models import Trajet, Reservation
from django.contrib.gis.geos import Point
from .forms import ProposeTripForm  # ton formulaire
from django.shortcuts import redirect, get_object_or_404



# Create your views here.
@login_required
def home(request):
    return render(request, 'Convoiturage/home.html')


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
                    return redirect('home') # Rediriger vers la page de profil
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
                return redirect('home')
            else:
                messages.error(request, 'Veuillez corriger les erreurs d\'inscription.')

    context = {
        'login_form': login_form,
        'registration_form': registration_form,
    }
    return render(request, 'Convoiturage/page_inscription.html', context)

# La vue de déconnexion reste la même
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('login_register')

@login_required
def settings(request):
    return render(request, 'Convoiturage/settings.html')  



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
     # Vérifier si l'utilisateur est un conducteur
    if  request.user.is_conducteur:
        messages.warning(request, "Vous devez être enregistré comme Utilisateur pour rechercher un trajet.")
        return redirect('profile') # Rediriger vers la page de profil pour changer de statut

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
            # Si la date est aujourd'hui, filtrer aussi par l'heuredz 
            if date_depart == today:
                queryset = queryset.filter(heure_depart__gte=now)
        else:
            # Si pas de date spécifique, trier les trajets à venir par pertinence (plus tôt = plus pertinent)
            queryset = queryset.order_by('date_depart', 'heure_depart')

        results = queryset.select_related('conducteur').all() # Optimisation pour récupérer les infos du conducteur

        if not results:
            messages.info(request, "Aucun trajet correspondant à votre recherche n'a été trouvé.")

    context = {
        'form': form,
        'results': results,
    }
    return render(request, 'Convoiturage/search_trip.html', context)





@login_required
def propose_trip_view(request):
    """
    Vue pour qu'un conducteur puisse proposer un trajet.
    """

    # Vérifier si l'utilisateur est un conducteur
    if not request.user.is_conducteur:
        messages.warning(request, "Vous devez être enregistré comme conducteur pour proposer un trajet.")
        return redirect('profile')  # Rediriger vers la page de profil

    if request.method == 'POST':
        form = ProposeTripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.conducteur = request.user  # Assigner le conducteur actuel

            # Récupérer les coordonnées GPS depuis les champs cachés
            origine_coords_str = request.POST.get('origine_coords')  # format : "lat,lng"
            destination_coords_str = request.POST.get('destination_coords')

            # Convertir les chaînes en Points GeoDjango
            if origine_coords_str:
                lat, lng = map(float, origine_coords_str.split(','))
                trip.origine_coords = Point(lng, lat)  # Point(lon, lat)

            if destination_coords_str:
                lat, lng = map(float, destination_coords_str.split(','))
                trip.destination_coords = Point(lng, lat)

            trip.save()
            messages.success(request, "Votre trajet a été proposé avec succès !")
            return redirect('home')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ProposeTripForm()

    return render(request, 'Convoiturage/propose_trip.html', {'form': form})


@login_required
def annonce(request):
    trajets = Trajet.objects.all().order_by('origine_coords', 'date_depart')  

    return render(request, 'Convoiturage/anonce.html', {
        'trajets': trajets
    })
@login_required
def historique(request):
    reservations = Reservation.objects.filter(Utilisateur=request.user).select_related('tra')
    return render(request, 'Convoiturage/reservation.html', {
        'reservations': reservations
    })




@login_required
def reserver_trajet(request, trajet_id):
    tra = get_object_or_404(Trajet, id=trajet_id)
    
    if  request.user.is_conducteur:
        messages.warning(request, "Vous devez être enregistré comme Utilisateur pour réserver un trajet.")
        return redirect('profile') # Rediriger vers la page de profil pour changer de statut

    if Reservation.objects.filter(Utilisateur=request.user, tra=tra).exists():
        messages.info(request, "Vous avez déjà réservé ce trajet.")
    else:
        Reservation.objects.create(Utilisateur=request.user, tra=tra)
        messages.success(request, "Trajet réservé avec succès !")

    return redirect('annonce')

