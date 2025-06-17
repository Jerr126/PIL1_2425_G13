from django import forms
from django.contrib.auth.hashers import make_password
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model # Pour obtenir votre modèle Utilisateur



Utilisateur = get_user_model() # Récupère le modèle Utilisateur défini dans settings.py

class UserRegistrationForm(UserCreationForm):
    # Les champs 'username', 'password', 'password_confirm' sont gérés par UserCreationForm
    # Nous ajoutons les champs supplémentaires de votre modèle Utilisateur

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    # Les autres champs seront rendus par Meta
    password_confirm = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'class': 'input-field-input'})
    )

    class Meta(UserCreationForm.Meta): # Hérite de Meta de UserCreationForm
        model = Utilisateur
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'num_tel',
            'email',
            'password', # Mot de passe
            'password_confirm', # Confirmation du mot de passe
            'is_conducteur',
            'type_vehicule',
            'matricule',
            'profile_picture', # Pour l'enregistrement, vous pouvez laisser l'utilisateur choisir une photo
        )
        # Personnalisez les widgets et labels comme vous le souhaitez
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Prénom', 'class': 'input-field-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'input-field-input'}),
            'num_tel': forms.TextInput(attrs={'placeholder': 'Numéro de téléphone (10 chiffres)', 'pattern': '\\d{10}', 'title': 'Le numéro doit contenir uniquement 10 chiffres.',
                                               'class': 'input-field-input'},),
            'type_vehicule': forms.TextInput(attrs={'placeholder': 'Type de véhicule', 'class': 'input-field-input'}),
            'matricule': forms.TextInput(attrs={'placeholder': 'Matricule', 'class': 'input-field-input'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'input-field-input'}),
            # Note: pour le mot de passe, UserCreationForm gère déjà le PasswordInput.
            # Pour profile_picture, Django gérera un FileInput par défaut.
        }
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'num_tel': 'Numéro de téléphone',
            'email': 'Email',
            'password': 'Mot de passe',
            'password_confirm': 'Confirmer le mot de passe',
            'is_conducteur': 'S\'inscrire en tant que conducteur ?',
            'type_vehicule': 'Type de véhicule (si conducteur)',
            'matricule': 'Matricule (si conducteur)',
            'profile_picture': 'Photo profil',
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
    username = forms.CharField(label="Prénoms", max_length=150, required=False) # Prénoms
    last_name = forms.CharField(label="Nom", max_length=150, required=False) # Nom
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
    
