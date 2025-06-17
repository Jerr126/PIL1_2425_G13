from django.contrib.gis.db import models
from django.core.validators import RegexValidator 
from django.contrib.auth.models import AbstractUser


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
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='profile_pics/profile.png')

    def str(self):
        # Utilise le nom complet s'il existe, sinon le nom d'utilisateur
        return self.get_full_name() or self.username




class Trajet(models.Model):
    id_trajet = models.AutoField(primary_key=True)
    point_depart = models.PointField()
    point_arrive = models.PointField()
    heure_depart = models.DateTimeField()
    duree = models.TimeField()
    place_libre = models.IntegerField()
    id_conducteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('heure_depart', 'id_conducteur')
        indexes = [
            models.Index(fields=['point_depart']),
            models.Index(fields=['point_arrive']),
        ]

