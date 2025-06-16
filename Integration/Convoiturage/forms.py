
from django import forms
from .models import Conducteur
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)



class ConducteurRegistrationForm(forms.ModelForm):
    # Ajoutez des champs supplémentaires si nécessaire, par exemple pour la confirmation du mot de passe
    password_confirm = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Veuillez confirmer votre mot de passe.'
    )

    class Meta:
        model = Conducteur
        fields = ['nom', 'prenom', 'num_tel', 'email', 'mot_de_passe', 'type_vehicule']
        widgets = {
            'mot_de_passe': forms.PasswordInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'num_tel': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'type_vehicule': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'num_tel': 'Numéro de téléphone',
            'mot_de_passe': 'Mot de passe',
            'email': 'Adresse e-mail',
            'type_vehicule': 'Type de véhicule',
        }
        help_texts = {
            'num_tel': 'Votre numéro de téléphone (10 chiffres).',
            'email': 'Votre adresse e-mail unique.',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('mot_de_passe')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        # Override save pour ne pas sauvegarder password_confirm
        conducteur = super().save(commit=False)
        # Ici, vous pourriez hasher le mot de passe avant de le sauvegarder
        # Pour cet exemple simple, nous le sauvegardons en clair, mais CE N'EST PAS SÉCURISÉ POUR LA PRODUCTION.
        # Utilisez des fonctions de hachage comme celles de Django pour les mots de passe réels.
        conducteur.mot_de_passe = make_password(self.cleaned_data['mot_de_passe'])
        if commit:
            conducteur.save()
        return conducteur