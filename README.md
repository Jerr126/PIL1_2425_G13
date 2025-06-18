PROJET INTEGRATEUR - 2024-2025 / IFRI_comotorage

Université : Université d’Abomey-Calavi 

Etablissement : Institut de Formation et de Recherche en Informatique (IFRI) 

Spécialité : Licence IA/IM/GL/SE&IoT/SI

Groupe n°13:
  - NATTA Itouta Yohanann Eldaa
  - BANDA BONI Charbel Seka
  - MEDJA Jerry Smith Nistelrooy
  - DADJI Naomie Kafuiata Océane
  - BOSSA Ghislain Régis Josaphat

DESCRIPTION:
Le projet de cette année consiste à réaliser une application web qui met en relation les étudiants de l’IFRI souhaitant partager leurs trajets quotidiens entre leur domicile et le campus. Dans cette application de covoiturage nommée ICE (Ifri Convoit Etudiant) :
  - Chaque utilisateur pourra créer un profil et l'éditer.
  - Il pourra agir en tant que simple passager ou conducteur.
  - Un passager pourra uniquement faire une recherche parmis les trajets disponibles et en réserver.
  - Un conduteur pourra seulement proposer un trajert .
  - les utilisateurs disposeront d'une maps qui leur montrera, une addresse suite à une recherche.
  - Chaque utilisateur aura accès à la liste des trajets disponibles et à l'historique des trajets avec lesquels, ils ont des liens (en tant que conducteur ou passager).
  - 




LANCEMENT (local) DU PROJET AVEC DJANGO:

pour ce faire suivre les étapes :
  - Cloner le dépôt Git : git clone votre_repo_github.git

  - Installer Python, PostgreSQL, PostGIS, GDAL, GEOS : l'installation de postGIS se fait avec celle de postgreSQL, les packages GDAL et GEOS ont obtenu à travers l'installation en mode avancé de l'app osgeo4w. 

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


FONCTIONNEMENT DE NOTRE APPLICATION ICE (Ifri Convoit Etudiant):

Après avoir lancer le server, l'accès à l'application la page de d'inscription et de connection, grâce à l'adresse  
http://127.0.0.1:8000/ définit par défaut sur django. L'accès a toute autre page est strictement restrincte par "@login_required" qui oblige que la connection au site soit effectuée.

Après l'enregistrement ou la connection, s'affichera la page d'acceuil, centre de notre application. Elle contient :
  - une barre de navigation, commune à toute les pages. Elle fait le liens entre toutes les pages de l'aplications.
  - une barre de recherche, qui permet à l'utilisateur de visualiser une address sur une maps juste en-dessous.
  - Ensuite on rencontre des zones qui mènent à la page d'annonce (affiche tous les trajets disponibles et permet uniquement à un passager d'en réserver), à la page historique (ouvre la liste de tous les trajets pris ou proposés), suivie d'une zone qui renvoie à la page de profil.
  - En fin le bas de page commun à toute les pages.

En cliquant sur le lien "rechercher un trajet" de la barre de navigation, seul un passager pourra accéder à la page seach_trip créer à pour la recherche. Dans le cas contraire, il sera redirigé vers la page de profil avec un message lui demandant de passer en mode Conducteur.

C'est le même principe pour le lien "proposer un trajet". Sur cette page, il disposera d'un formulaire et d'une maps qui lui montrera le trajet qu'il souhaite proposer, s'il le veut.

Sur la page de profil, l'Utilisateur aurra accès à ses informations personnelles et pourra les éditer. 



Sécurité et confidentialité :
La confidencialité et la sécurité sont assurées grâce à des fonctions qui hachent le mot de passe, et n'autorise l'accès à ue page que si l'utulisateur est connecté.