PROJET INTEGRATEUR - 2024-2025 / IFRI_comotorage

Université : Université d’Abomey-Calavi 

Etablissement : Institut de Formation et de Recherche en Informatique (IFRI) 

Spécialité : Licence IA/IM/GL/SE&IoT/SI

Groupe n°13:
  - NATTA Itouta Yohanann Eldaa
  - BANDA BONI Charbel Seka
  - MEDJA Jerry Smith Nistelrooy
  - DADJI Naomie Kafuiata Océane

DESCRIPTION:
Le projet de cette année consiste à réaliser une application web qui met en relation les étudiants de l’IFRI souhaitant partager leurs trajets quotidiens entre leur domicile et le campus. Dans cette application de covoiturage nommée ICE (Ifri Convoit Etudiant) :
  - Chaque utilisateur pourra de créer un profil et de pouvoir agir en tant que simple passager ou conducteur.
  - Un passager pourra faire une recherche parmis les trajets disponibles et en sélectionner.
  - Un conduteur pourra proposer un trajert et verrifier les passagers ayant faits des réservations.
  - les utilisateurs disposeront d'une maps qui leur montrera, une addresse suite à une recherche ou un trajet.



LANCEMENT (local) DU PROJET AVEC DJANGO:

pour ce faire suivre les étapes :
  - Cloner le dépôt Git : git clone votre_repo_github.git

  - Installer Python, PostgreSQL, PostGIS, GDAL, GEOS : 

  - Créer et activer un environnement virtuel. Pour ce faire:
      1. Naviguer vers le répertoire de votre projet
      2. Créer l'environnement virtuel grâce à la commande python -m venv venv, le 2èmes venv étant le nom de l'environement
      3. Activer l'environnement virtuel par 
      (.\venv\Scripts\activate sur windows) ou (source venv/bin/activate sur linus ou macOS)

  - Installer les dépendances Python : pip install -r requirements.txt

  - Créer la base de données et l'utilisateur PostgreSQL et activer l'extension PostGIS  dans votre base de données (CREATE EXTENSION postgis;). N'oubliez pas remplacer les informations de la base de données dans settings.py

  - Mettre à jour settings.py : Assurez-vous que DATABASES et les chemins GDAL/GEOS sont corrects pour ce nouvel appareil.

  - Exécuter les migrations : python manage.py migrate

  - Créer un superutilisateur : python manage.py createsuperuser

  - Lancer le serveur de développement : python manage.py runserver


