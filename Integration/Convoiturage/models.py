from django.contrib.gis.db import models
from django.core.validators import RegexValidator 

# Create your models here.
class Conducteur(models.Model):
    id_conducteur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\d{10}$', # Regex pour 10 chiffres exacts. Si vous voulez plus de flexibilité, utilisez r'^\d+$'
        message="uniquement 10 chiffres."
    )
    num_tel = models.CharField(
        validators=[phone_regex], # Applique le validateur
        unique=True,
        max_length=10 # Conserve max_length à 10 pour la cohérence
    )
    mot_de_passe = models.CharField(max_length=180)
    email = models.EmailField(unique=True)
    type_vehicule = models.CharField(max_length=100)


class Trajet(models.Model):
    id_trajet = models.AutoField(primary_key=True)
    point_depart = models.PointField()
    point_arrive = models.PointField()
    heure_depart = models.DateTimeField()
    duree = models.TimeField()
    place_libre = models.IntegerField()
    id_conducteur = models.ForeignKey(Conducteur, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('heure_depart', 'id_conducteur')
        indexes = [
            models.Index(fields=['point_depart']),
            models.Index(fields=['point_arrive']),
        ]


class Passager(models.Model):
    id_passager = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=100)
    phone_regex = RegexValidator(
        regex=r'^\d{10}$', # Regex pour 10 chiffres exacts. Si vous voulez plus de flexibilité, utilisez r'^\d+$'
        message="uniquement 10 chiffres."
    )
    num_tel = models.CharField(
        validators=[phone_regex], # Applique le validateur
        unique=True,
        max_length=10 # Conserve max_length à 10 pour la cohérence
    )
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=180)
    id_conducteur = models.ForeignKey(Conducteur, on_delete=models.CASCADE)
    id_trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    


