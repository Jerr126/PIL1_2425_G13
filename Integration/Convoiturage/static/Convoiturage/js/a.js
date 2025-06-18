// assets/js/a.js

// --- Variables globales (moins utilisées avec Django, car le backend gère les données utilisateur) ---
// userMode et userName sont maintenant gérés par Django et passés au template via le contexte.
// Si vous avez besoin de ces valeurs en JS, passez-les depuis le template Django via des attributs data-*
// ou des variables globales définies dans le template avec {% if user.is_authenticated %}<script>let userName = "{{ user.username }}";</script>{% endif %}
// let userMode = "passenger"; // Géré par Django via user.is_conducteur
// let userName = "Marie";     // Géré par Django via user.username ou user.first_name

// publishedRides : Cette variable stockait les trajets publiés côté client.
// Avec Django, les trajets sont stockés dans la base de données et récupérés/affichés par les vues.
// let publishedRides = [];

// --- Éléments du DOM pour le menu mobile (commenté car non présent dans le HTML fourni, mais peut être réactivé si besoin) ---
// const mobileMenuBtn = document.getElementById('mobileMenuBtn');
// const menuSpace = document.getElementById('menuSpace');

// --- Gestion du menu mobile (si vous en avez un) ---
// if (mobileMenuBtn) {
//     mobileMenuBtn.addEventListener('click', toggleMenu);
// }

// document.addEventListener('click', (e) => {
//   if (menuSpace && mobileMenuBtn && !menuSpace.contains(e.target) && e.target !== mobileMenuBtn) {
//     closeMenu();
//   }
// });

// function toggleMenu() {
//   if (menuSpace) {
//     menuSpace.classList.toggle('active');
//   }
// }

// function closeMenu() {
//   if (menuSpace) {
//     menuSpace.classList.remove('active');
//   }
// }


// --- Gestion de la barre de navigation Ionicons ---
// Cette partie est cruciale pour le comportement visuel de votre barre de navigation.
// Elle n'est plus gérée par ce script JS puisque la classe 'active' est ajoutée côté Django dans le base.html.
// Cependant, vous pourriez la conserver si vous voulez des effets visuels supplémentaires au clic.
const list = document.querySelectorAll('.list');

function activeLink() {
    // Cette fonction n'est utile que si vous voulez un indicateur visuel dynamique au clic,
    // en plus de l'indicateur géré par Django au chargement de la page.
    // Si la page est rechargée après un clic, la logique Django reprend le contrôle.
    list.forEach((item) => item.classList.remove('active'));
    this.classList.add('active');
}
list.forEach((item) => item.addEventListener('click', activeLink));


// --- Fonctions de gestion des popups (celles qui sont encore nécessaires) ---

// Fonction pour afficher une popup donnée par son ID.
// Utilisée pour la popup de "changement de mode" et la "publication réussie".
function showPopup(id) {
    const popupElement = document.getElementById(id);
    if (popupElement) {
        popupElement.style.display = "flex"; // Affiche la popup
        document.body.style.overflow = "hidden"; // Empêche le défilement de la page derrière la popup
    }
}

// Fonction pour fermer la popup de "changement de mode".
function closePopup() {
    const popupElement = document.getElementById('popup');
    if (popupElement) {
        popupElement.style.display = "none"; // Cache la popup
        document.body.style.overflow = "auto"; // Réactive le défilement de la page
    }
}

// Fonction pour fermer la popup de succès de publication.
function closePublishSuccessPopup() {
    const popupElement = document.getElementById('publishSuccessPopup');
    if (popupElement) {
        popupElement.style.display = "none"; // Cache la popup
        document.body.style.overflow = "auto"; // Réactive le défilement de la page
    }
}

// Fonctions pour ouvrir/fermer les popups de recherche et de publication
// Ces fonctions ne sont plus appelées directement par les boutons principaux
// du HTML d'accueil si ces boutons redirigent vers des pages Django.
// Elles sont utiles si vous souhaitez que les popups restent des modales sur la même page.

function openSearchPopup() {
    showPopup('searchPopup');
    // Pré-remplir la date et l'heure actuelles (si le formulaire n'est pas rempli par Django)
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    const now = new Date();
    now.setHours(now.getHours() + 1); // Heure actuelle + 1h
    document.getElementById('time').value = now.toTimeString().substring(0, 5);
}

function closeSearchPopup() {
    const popupElement = document.getElementById('searchPopup');
    if (popupElement) {
        popupElement.style.display = "none";
        document.body.style.overflow = "auto";
    }
}

function openPublishPopup() {
    showPopup('publishPopup');
    // Pré-remplir la date et l'heure actuelles (si le formulaire n'est pas rempli par Django)
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('publishDate').value = today;
    const now = new Date();
    now.setHours(now.getHours() + 1); // Heure actuelle + 1h
    document.getElementById('publishTime').value = now.toTimeString().substring(0, 5);
}

function closePublishPopup() {
    const popupElement = document.getElementById('publishPopup');
    if (popupElement) {
        popupElement.style.display = "none";
        document.body.style.overflow = "auto";
    }
}


// --- Fonctions JavaScript pour les actions (recherche, publication) ---
// Ces fonctions sont maintenant censées interagir avec le backend Django.
// Elles ne manipulent plus directement des tableaux JS ou le localStorage.

// Fonction pour la recherche d'un trajet (appelée par le bouton dans la popup de recherche)
function performSearch() {
    const departure = document.getElementById('departure').value.trim();
    const arrival = document.getElementById('arrival').value.trim();
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const passengers = document.getElementById('passengers').value;

    if (!departure || !arrival) {
        showAlert('Veuillez indiquer au moins une ville de départ et une destination.');
        return;
    }

    // Ici, au lieu d'afficher une alerte, vous feriez une requête AJAX à une vue Django
    // ou vous redirigeriez l'utilisateur vers une page de résultats avec les paramètres de recherche.
    // Exemple de redirection (plus simple à mettre en place initialement) :
    // Construisez l'URL de recherche avec les paramètres
    const searchUrl = `/search/?departure=${encodeURIComponent(departure)}&arrival=${encodeURIComponent(arrival)}&date=${date}&time=${time}&passengers=${passengers}`;
    window.location.href = searchUrl;

    // Ou si vous voulez une requête AJAX (plus complexe, nécessiterait une vue API et un affichage dynamique)
    /*
    fetch('/api/search_trips/', {
        method: 'POST', // Ou GET si les paramètres sont dans l'URL
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Fonction pour obtenir le CSRF token
        },
        body: JSON.stringify({ departure, arrival, date, time, passengers })
    })
    .then(response => response.json())
    .then(data => {
        // Traiter les résultats de la recherche (par exemple, afficher une liste de trajets)
        console.log('Résultats de la recherche :', data);
        closeSearchPopup();
    })
    .catch(error => {
        console.error('Erreur lors de la recherche :', error);
        showAlert('Une erreur est survenue lors de la recherche.');
    });
    */
}

// Fonction pour publier un trajet (appelée par le bouton dans la popup de publication)
function publishRide() {
    const departure = document.getElementById('publishDeparture').value.trim();
    const arrival = document.getElementById('publishArrival').value.trim();
    const date = document.getElementById('publishDate').value;
    const time = document.getElementById('publishTime').value;
    const seats = document.getElementById('publishSeats').value;
    const price = document.getElementById('publishPrice').value;
    const car = document.getElementById('publishCar').value.trim();

    if (!departure || !arrival || !car) {
        showAlert('Veuillez remplir tous les champs obligatoires.');
        return;
    }

    // Ici, vous enverriez les données à une vue Django via AJAX.
    // Cela nécessite une vue Django qui gère la soumission du formulaire de trajet.
    // Exemple d'utilisation de Fetch API pour envoyer les données :
    fetch('propose-trip/', { // Assurez-vous que cette URL est correcte et pointe vers votre vue Django
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Fonction utilitaire pour obtenir le CSRF token
        },
        body: JSON.stringify({
            origine: departure, // Adaptez les noms de champs à ceux de votre modèle Django
            destination: arrival,
            date_depart: date,
            heure_depart: time,
            nombre_places: seats,
            prix_par_place: price,
            modele_voiture: car // Ajoutez ce champ à votre modèle Trajet si nécessaire
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json(); // Ou response.text() si la vue renvoie du texte
        }
        throw new Error('Erreur réseau ou réponse non OK.');
    })
    .then(data => {
        console.log('Réponse du serveur :', data);
        closePublishPopup();
        showPopup('publishSuccessPopup'); // Affiche la popup de succès
        // Vous pouvez aussi recharger la page ou rediriger ici si nécessaire
        // window.location.reload();
    })
    .catch(error => {
        console.error('Erreur lors de la publication du trajet :', error);
        showAlert('Une erreur est survenue lors de la publication de votre trajet.');
    });
}


// --- Fonctions utilitaires ---

// Fonction pour obtenir le CSRF token (indispensable pour les requêtes POST/PUT/DELETE AJAX avec Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// showAlert() peut être conservée si vous souhaitez des alertes JavaScript pour des feedbacks non critiques.
function showAlert(message) {
    alert(message);
}

// formatDate() peut être utile si vous avez besoin de formater des dates côté client pour l'affichage.
function formatDate(dateString) {
    const options = { weekday: 'long', day: 'numeric', month: 'long' };
    return new Date(dateString).toLocaleDateString('fr-FR', options);
}


// --- Animations et initialisation au chargement du DOM ---
document.addEventListener('DOMContentLoaded', () => {
    animateElements(); // Appelle la fonction d'animation au chargement

    // Gérer l'état initial de la barre de navigation (la classe 'active')
    // C'est mieux géré dans le template Django avec {% if request.resolver_match.url_name == 'accueil' %}active{% endif %}
    // Mais si vous avez une logique JS pour cela, vous pouvez la mettre ici.
    // Par exemple, si vous voulez que la barre Ionicons ait une animation différente au chargement.

    // Gérer le placeholder de la barre de recherche.
    // Si 'userName' est passé globalement depuis le template Django :
    /*
    const searchInput = document.querySelector('.search-bar input');
    if (searchInput && typeof userName !== 'undefined') {
        searchInput.placeholder = `${userName}, où souhaitez-vous aller aujourd'hui ?`;
    } else if (searchInput) {
        searchInput.placeholder = `Où souhaitez-vous aller aujourd'hui ?`; // Placeholder générique
    }
    */

    // Ajout des écouteurs d'événements pour les boutons "Trouver un trajet" et "Proposer un trajet"
    // S'ils ne redirigent pas directement, mais ouvrent une popup modale.
    const findTripBtn = document.querySelector('.main-buttons button:first-child');
    const publishTripBtn = document.querySelector('.main-buttons button:last-child');

    if (findTripBtn) {
        findTripBtn.onclick = openSearchPopup; // Ouvre la popup de recherche
    }

    if (publishTripBtn) {
        // Pour le bouton "Proposer un trajet", nous devons vérifier le statut conducteur.
        // Cette logique doit être passée depuis Django.
        // Exemple : un attribut data-conducteur-status sur le body ou un script intégré.
        const isConducteur = document.body.dataset.isConducteur === 'true'; // Récupérer depuis un attribut data-
        
        publishTripBtn.onclick = () => {
            if (isConducteur) {
                openPublishPopup(); // Ouvre la popup de publication
            } else {
                showPopup('popup'); // Ouvre la popup "changer de mode"
            }
        };
    }
});


// Fonction pour les animations d'éléments au chargement.
// Utile pour un effet visuel agréable.
function animateElements() {
    const elements = document.querySelectorAll('.search-bar, .map-container, .main-buttons, .feature-card');

    elements.forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.animation = `fadeInUp 0.5s ease-out ${i * 0.1}s forwards`;
    });

    // Ajout du CSS pour l'animation (peut être déplacé dans un fichier CSS si vous préférez)
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInUp {
            to { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);
}