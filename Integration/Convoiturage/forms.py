from django import forms
from django.contrib.auth.hashers import make_password
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model # Pour obtenir votre modèle Utilisateur
from .models import Trajet
from datetime import datetime, date


Utilisateur = get_user_model() # Récupère le modèle Utilisateur défini dans settings.py

class UserRegistrationForm(UserCreationForm):
    # Les champs 'username', 'password', 'password_confirm' sont gérés par UserCreationForm
    # Nous ajoutons les champs supplémentaires de votre modèle Utilisateur

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    # Les autres champs seront rendus par Meta


    class Meta(UserCreationForm.Meta): # Hérite de Meta de UserCreationForm
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'username', # Nom d'utilisateur
            'num_tel',
            'email',
            'is_conducteur',
            'type_vehicule',
            'matricule',
        )
        # Personnalisez les widgets et labels comme vous le souhaitez
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Prénom', 'class': 'input-field-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'input-field-input'}),
            'username': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'class': 'input-field-input'}),
            'num_tel': forms.TextInput(attrs={'placeholder': 'Numéro de téléphone (10 chiffres)', 'pattern': '\\d{10}', 'title': 'Le numéro doit contenir uniquement 10 chiffres.',
                                               'class': 'input-field-input'},),
            'type_vehicule': forms.TextInput(attrs={'placeholder': 'Type de véhicule', 'class': 'input-field-input'}),
            'matricule': forms.TextInput(attrs={'placeholder': 'Matricule', 'class': 'input-field-input'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'input-field-input'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'class': 'input-field-input'}),
            # Note: pour le mot de passe, UserCreationForm gère déjà le PasswordInput.
            # Pour profile_picture, Django gérera un FileInput par défaut.
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'username': 'Nom d\'utilisateur',
            'num_tel': 'Numéro de téléphone',
            'email': 'Email',
            'password1': 'Mot de passe',
            'password2': 'Confirmer le mot de passe',
            'is_conducteur': 'S\'inscrire en tant que conducteur ?',
            'type_vehicule': 'Type de véhicule (si conducteur)',
            'matricule': 'Matricule (si conducteur)',
        }

    # Vous pouvez ajouter une logique de nettoyage supplémentaire ici si nécessaire
    def clean(self):
        cleaned_data = super().clean()
        is_conducteur = cleaned_data.get('is_conducteur')
        type_vehicule = cleaned_data.get('type_vehicule')
        matricule = cleaned_data.get('matricule')

        if is_conducteur:
            if not type_vehicule:
                self.add_error('type_vehicule', "Le type de véhicule est requis pour les conducteurs.")
            if not matricule:
                self.add_error('matricule', "Le matricule est requis pour les conducteurs.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Ici, vous pouvez ajouter une logique spécifique avant de sauvegarder l'utilisateur,
        user.set_password(self.cleaned_data["password"]) # Utilisez set_password pour hacher
        if commit:
            user.save()
        return user

class ConnexionForm(AuthenticationForm):
    # Cette classe reste la même, elle gère la connexion pour n'importe quel modèle User
    username = forms.CharField(label="Email ou Nom d'utilisateur", widget=forms.TextInput(attrs={'placeholder': 'Email ou Nom d\'utilisateur'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))    


class UtilisateurProfileForm(forms.ModelForm):
    # Les labels sont définis ici pour correspondre à votre HTML
    first_name = forms.CharField(label="Prénoms", max_length=150, required=False) # Prénoms
    last_name = forms.CharField(label="Nom", max_length=150, required=False) # Nom
    username = forms.CharField(label="Nom d'utilisateur", max_length=150, required=True) # Nom d'utilisateur
    email = forms.EmailField(label="Email", required=True)
    num_tel = forms.CharField(label="Numéro de téléphone", max_length=10, required=True)

    is_conducteur = forms.BooleanField(label="Activer le statut de Conducteur", required=False)
    type_vehicule = forms.CharField(label="Type d'engin", max_length=100, required=False)
    matricule = forms.CharField(label="Matricule", max_length=50, required=False)

    profile_picture = forms.ImageField(label="Photo de profil", required=False)

    class Meta:
        model = Utilisateur
        fields = [
            'username', 'last_name', 'email', 'num_tel',
            'is_conducteur', 'type_vehicule', 'matricule', 
            'profile_picture'
        ]
        # Vous pouvez ajouter des widgets si vous avez besoin de classes CSS spécifiques ou d'attributs HTML
        # widgets = {
        #     'first_name': forms.TextInput(attrs={'class': 'my-input-class'}),
        # }

    def clean(self):
        cleaned_data = super().clean()
        is_conducteur = cleaned_data.get('is_conducteur')
        type_vehicule = cleaned_data.get('type_vehicule')
        matricule = cleaned_data.get('matricule')


        # Validation conditionnelle : Si conducteur, ces champs sont obligatoires
        if is_conducteur:
            if not type_vehicule:
                self.add_error('type_vehicule', "Le type d'engin est obligatoire pour un conducteur.")
            if not matricule:
                self.add_error('matricule', "Le matricule est obligatoire pour un conducteur.")

        else:
            # Si l'utilisateur n'est PAS conducteur, effacer les valeurs de ces champs
            cleaned_data['type_vehicule'] = ""
            cleaned_data['matricule'] = ""

        return cleaned_data
    
class ProposeTripForm(forms.ModelForm):
    class Meta:
        model = Trajet
        fields = [
            'origine', 'destination', 'date_depart', 'heure_depart',
            'nombre_places', 'prix_par_place', 'description'
        ]
        widgets = {
            'date_depart': forms.DateInput(attrs={'type': 'date'}),
            'heure_depart': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_depart = cleaned_data.get('date_depart')
        heure_depart = cleaned_data.get('heure_depart')

        if date_depart and heure_depart:
            # Combiner date et heure pour une comparaison complète
            depart_datetime = datetime.combine(date_depart, heure_depart)
            # Vérifier que le trajet n'est pas dans le passé
            if depart_datetime < datetime.now():
                raise forms.ValidationError("La date et l'heure de départ ne peuvent pas être dans le passé.")
        return cleaned_data


class TrajetSearchForm(forms.Form):
    origine = forms.CharField(max_length=255, label="Lieu de départ", required=True)
    destination = forms.CharField(max_length=255, label="Lieu d'arrivée", required=True)
    date_depart = forms.DateField(
        label="Date de départ",
        widget=forms.DateInput(attrs={'type': 'date'}), # Widget HTML5 pour le calendrier
        required=False # Optionnel, pour permettre une recherche plus large
    )
    # L'heure peut être une option de filtre avancé, ou omise pour simplifier
    # heure_depart = forms.TimeField(
    #     label="Heure de départ (proche de)",
    #     widget=forms.TimeInput(attrs={'type': 'time'}),
    #     required=False
    # )
    nombre_places_min = forms.IntegerField(
        label="Nombre de places requises",
        min_value=1,
        initial=1,
        required=False
    )

    # Vous pouvez ajouter des champs pour la "position" si vous utilisez des coordonnées
    # latitude = forms.DecimalField(...)
    # longitude = forms.DecimalField(...)
    # rayon_recherche = forms.IntegerField(...)