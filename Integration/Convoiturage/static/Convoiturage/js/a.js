// assets/js/a.js

// --- Variables globales (moins utilisées avec Django, car le backend gère les données utilisateur) ---
// userMode et userName sont maintenant gérés par Django et passés au template via le contexte.
// let userMode = "passenger"; // Géré par Django via user.is_conducteur
// let userName = "Marie";     // Géré par Django via user.username ou user.first_name

// publishedRides : Cette variable stockait les trajets publiés côté client.
// Avec Django, les trajets sont stockés dans la base de données et récupérés/affichés par les vues.
// let publishedRides = []; 


// --- Éléments du DOM pour le menu mobile (ces IDs doivent être présents dans votre HTML si vous utilisez cette logique) ---
// Ces variables ne sont nécessaires que si vous avez un menu mobile séparé de la navigation principale.
// Si votre navigation est gérée entièrement par la barre Ionicons dans home.html, vous pouvez commenter/supprimer ces lignes
// et les fonctions associées (toggleMenu, closeMenu).
// const mobileMenuBtn = document.getElementById('mobileMenuBtn');
// const menuSpace = document.getElementById('menuSpace');


// --- Gestion du menu mobile (si vous en avez un) ---
// mobileMenuBtn.addEventListener('click', toggleMenu);

// // Fermer le menu en cliquant à l'extérieur
// document.addEventListener('click', (e) => {
//   if (menuSpace && mobileMenuBtn && !menuSpace.contains(e.target) && e.target !== mobileMenuBtn) {
//     closeMenu();
//   }
// });

// function toggleMenu() {
//   if (menuSpace) {
//     menuSpace.classList.toggle('active');
//   }
// }

// function closeMenu() {
//   if (menuSpace) {
//     menuSpace.classList.remove('active');
//   }
// }


// --- Gestion de la barre de navigation Ionicons ---
// Cette partie est cruciale pour le comportement visuel de votre barre de navigation.
const list = document.querySelectorAll('.list'); // Sélectionne tous les éléments avec la classe 'list' (vos liens de navigation)

function activeLink() {
    // Supprime la classe 'active' de tous les éléments 'list'
    list.forEach((item) => item.classList.remove('active'));
    // Ajoute la classe 'active' à l'élément sur lequel on a cliqué
    this.classList.add('active');
}
// Ajoute un écouteur d'événement 'click' à chaque élément 'list' pour appeler 'activeLink'
list.forEach((item) => item.addEventListener('click', activeLink));


// --- Fonctions de gestion des popups (celles qui sont encore nécessaires) ---

// Fonction pour afficher une popup donnée par son ID.
// Utilisée pour la popup de "changement de mode" et la "publication réussie" si vous la conservez.
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

// Fonction pour fermer la popup de succès de publication (si vous la gardez).
function closePublishSuccessPopup() {
    const popupElement = document.getElementById('publishSuccessPopup');
    if (popupElement) {
        popupElement.style.display = "none"; // Cache la popup
        document.body.style.overflow = "auto"; // Réactive le défilement de la page
    }
}

// --- Fonctions JavaScript liées à la logique de "Proposer un trajet" et "Rechercher un trajet" ---
// Ces fonctions sont maintenant gérées directement par les redirections dans home.html vers les vues Django dédiées.
// Par conséquent, elles sont commentées ou adaptées.

// Ancien: handleSearch() ouvrait une popup de recherche.
// Nouveau: Le bouton "Trouver un trajet" dans home.html redirige directement vers {% url 'search_trip' %}.
/*
function handleSearch() {
    showPopup('searchPopup');
    // Pré-remplir la date du jour et l'heure (cette logique est maintenant mieux gérée directement dans le formulaire Django si besoin)
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    const now = new Date();
    now.setHours(now.getHours() + 1);
    document.getElementById('time').value = now.toTimeString().substring(0, 5);
}
*/

// Ancien: handlePublish() ouvrait la popup de publication ou la popup de "changement de mode".
// Nouveau: Cette logique est maintenant gérée par la fonction 'checkConducteurStatus()' directement dans <script> de home.html.
/*
function handlePublish() {
    // userMode n'est plus une variable JS, mais un statut Django via 'user.is_conducteur'
    // Cette logique est déplacée dans le JavaScript intégré à home.html pour utiliser le contexte Django.
    // Si l'utilisateur est passager, on ouvre la popup 'popup' (changement de mode).
    // Sinon, on ouvre la popup de publication (qui est maintenant une redirection vers une page Django).
}
*/

// Ancien: showPublishPopup() ouvrait la popup de publication.
// Nouveau: Le bouton "Proposer un trajet" redirige directement vers {% url 'propose_trip' %} après vérification du statut.
/*
function showPublishPopup() {
    // Pré-remplir la date et l'heure (cette logique est maintenant mieux gérée directement dans le formulaire Django si besoin)
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('publishDate').value = today;
    const now = new Date();
    now.setHours(now.getHours() + 1);
    document.getElementById('publishTime').value = now.toTimeString().substring(0, 5);
    showPopup('publishPopup');
}
*/

// Ancien: closePublishPopup() fermait la popup de publication.
// Nouveau: Non nécessaire, car nous redirigeons vers une autre page.
/*
function closePublishPopup() {
    document.getElementById('publishPopup').style.display = "none";
    document.body.style.overflow = "auto";
}
*/

// Ancien: publishRide() gérait la logique de publication côté client (création d'objet, localStorage).
// Nouveau: Cette logique est entièrement gérée par la vue Django (propose_trip_view) et le formulaire Django.
/*
function publishRide() {
    const departure = document.getElementById('publishDeparture').value.trim();
    const arrival = document.getElementById('publishArrival').value.trim();
    const date = document.getElementById('publishDate').value;
    const time = document.getElementById('publishTime').value;
    const seats = document.getElementById('publishSeats').value;
    const price = document.getElementById('publishPrice').value;
    const car = document.getElementById('publishCar').value.trim();
    
    if (!departure || !arrival || !car) {
        showAlert('Veuillez remplir tous les champs obligatoires');
        return;
    }
    
    const newRide = {
        id: Date.now(),
        driver: userName, // userName viendrait de Django maintenant
        from: departure,
        to: arrival,
        date: formatDate(date),
        time: time,
        seats: seats,
        availableSeats: seats,
        price: price,
        car: car,
        publishedAt: new Date().toLocaleString()
    };
    
    publishedRides.unshift(newRide);
    console.log('Trajet publié :', newRide);
    
    saveRidesToLocalStorage(); // Plus nécessaire avec une DB Django
    
    closePublishPopup();
    showPopup('publishSuccessPopup');
}
*/

// Ancien: saveRidesToLocalStorage() et loadRidesFromLocalStorage() géraient la persistance côté client.
// Nouveau: Les données sont maintenant stockées dans la base de données via Django.
/*
function saveRidesToLocalStorage() {
    localStorage.setItem('publishedRides', JSON.stringify(publishedRides));
}

function loadRidesFromLocalStorage() {
    const rides = localStorage.getItem('publishedRides');
    if (rides) {
        publishedRides = JSON.parse(rides);
    }
}
*/

// Ancien: closeSearchPopup() fermait la popup de recherche.
// Nouveau: Non nécessaire, car nous redirigeons vers une autre page.
/*
function closeSearchPopup() {
    document.getElementById('searchPopup').style.display = "none";
    document.body.style.overflow = "auto";
}
*/

// Ancien: redirectToProfile() redirigeait vers un fichier HTML statique.
// Nouveau: La redirection est gérée directement dans home.html avec {% url 'profile' %}.
/*
function redirectToProfile() {
    sessionStorage.setItem('redirectAfterProfile', 'publish.html'); // Cette logique n'est plus pertinente
    window.location.href = "profile.html"; // Utilisez {% url 'profile' %} dans le template
}
*/

// Ancien: performSearch() gérait la recherche côté client et l'affichage d'une alerte.
// Nouveau: Cette logique est entièrement gérée par la vue Django (search_trip_view) et le formulaire Django.
/*
function performSearch() {
    const departure = document.getElementById('departure').value.trim();
    const arrival = document.getElementById('arrival').value.trim();
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const passengers = document.getElementById('passengers').value;
    
    if (!departure || !arrival) {
        showAlert('Veuillez indiquer au moins une ville de départ et une destination');
        return;
    }
    
    const searchData = {
        from: departure,
        to: arrival,
        date: formatDate(date),
        time: time,
        seats: passengers
    };
    
    console.log('Recherche lancée :', searchData);
    closeSearchPopup();
    showAlert(`Recherche effectuée :\nDe ${searchData.from} à ${searchData.to}\nLe ${searchData.date} à ${searchData.time}\nPlaces : ${searchData.seats}`);
}
*/

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

    // Simuler un temps de chargement et personnaliser le placeholder de la barre de recherche.
    // userName est maintenant un contexte Django, donc cette ligne devrait être mise à jour
    // pour que le placeholder soit défini directement dans le HTML avec {{ user.username }}
    // ou passé en JS via une variable globale si absolument nécessaire.
    /*
    setTimeout(() => {
        const searchInput = document.querySelector('.search-bar input');
        if (searchInput) {
            // userName n'est pas accessible directement ici depuis Django.
            // Il faudrait le passer via un attribut data- ou une variable globale dans le template.
            // Pour l'instant, on peut laisser un placeholder générique ou le récupérer si userName est exposé globalement.
            // searchInput.placeholder = `${userName}, où souhaitez-vous aller aujourd'hui ?`;
            searchInput.placeholder = `Où souhaitez-vous aller aujourd'hui ?`; // Placeholder générique
        }
    }, 1000);
    */
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