from django.contrib.gis.db import models

# Create your models here.
class Conducteur(models.Model):
    id_conducteur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=100)
    num_tel = models.CharField(unique=True, max_length=10)
    mot_de_passe = models.CharField(max_length=50)
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
    num_tel = models.CharField(unique=True, max_length=10)
    mot_de_passe = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    id_conducteur = models.ForeignKey(Conducteur, on_delete=models.CASCADE)
    id_trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    


