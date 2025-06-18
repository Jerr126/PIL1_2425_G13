from django.contrib.gis.db import models
from django.core.validators import RegexValidator 
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Pour lier à notre modèle d'utilisateur personnalisé
from datetime import datetime



class Utilisateur(AbstractUser):
    # Les champs 'first_name', 'last_name', 'username', 'password' sont déjà dans AbstractUser.

    # Assurez-vous que l'email est unique et obligatoire
    email = models.EmailField(unique=True, blank=False, null=False)

    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="uniquement 10 chiffres."
    )
    num_tel = models.CharField(
        validators=[phone_regex],
        unique=True,
        max_length=10,
        blank=False, # Rend le numéro de tel optionnel si l'utilisateur ne le fournit pas initialement
        null=True
    )

    # Champs pour le rôle
    is_conducteur = models.BooleanField(default=False)
    # is_passager est implicite si !is_conducteur dans ce cas.
    # Si vous voulez qu'un utilisateur puisse être les deux, gardez un champ is_passager.

    # Champs spécifiques au conducteur
    type_vehicule = models.CharField(max_length=100, blank=True, null=True) # Type d'engin
    matricule = models.CharField(max_length=50, blank=True, null=True)

    # Photo de profil
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/profile.jpg')

    def str(self):
        # Utilise le nom complet s'il existe, sinon le nom d'utilisateur
        return self.get_full_name() or self.username


# Assurez-vous que votre modèle Utilisateur est importé ou référencé correctement
# from .models import Utilisateur # Si Utilisateur est dans le même fichier

class Trajet(models.Model):
    # Lien vers le conducteur (utilisateur personnalisé)
    conducteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trajets_proposes',
        default=1,
        limit_choices_to={'is_conducteur': True} # S'assurer que seul un conducteur peut proposer un trajet
    )

    origine = models.CharField(verbose_name="Lieu de départ", null=True, blank=True)
    destination = models.CharField(verbose_name="Lieu d'arrivée", null=True, blank=True)
    origine_coords = models.PointField(null=True, blank=True)
    destination_coords = models.PointField(null=True, blank=True)
    date_depart = models.DateField(verbose_name="Date de départ")
    heure_depart = models.TimeField(verbose_name="Heure de départ")
    nombre_places = models.PositiveIntegerField(default=0, verbose_name="places disponibles")
    prix_par_place = models.PositiveIntegerField(default=200, verbose_name="Prix par place")
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True, verbose_name="Trajet actif")

    class Meta:
        verbose_name = "Trajet"
        verbose_name_plural = "Trajets"
        ordering = ['date_depart', 'heure_depart'] # Tri par défaut

    def __str__(self):
        return f"Trajet de {self.origine} à {self.destination} le {self.date_depart} par {self.conducteur.get_full_name() or self.conducteur.username}"

    # Propriété pour combiner date et heure pour des comparaisons plus faciles
    @property
    def datetime_depart(self):
        return datetime.combine(self.date_depart, self.heure_depart)


class Reservation(models.Model):
    Utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tra = models.ForeignKey('Trajet', on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('Utilisateur', 'tra')  # Empêche la double réservation
