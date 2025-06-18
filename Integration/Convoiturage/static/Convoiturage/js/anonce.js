

// Fonction pour afficher toutes les annonces
function afficherToutesLesAnnonces() {
   
    // pas du localStorage. Pour l'exemple, nous gardons localStorage.
    const annonces = JSON.parse(localStorage.getItem("annoncesConducteurs") || "[]");
    const conteneur = document.getElementById("listeAnnonces");
    conteneur.innerHTML = ""; // Vide le conteneur avant d'ajouter de nouvelles annonces

    if (annonces.length === 0) {
        conteneur.innerHTML = "<p style='text-align:center;'>Aucune annonce disponible pour le moment.</p>";
        return;
    }

    annonces.forEach((a, index) => {
        const div = document.createElement("div");
        div.className = "annonce";
        // Utilisation de template literals pour un HTML plus propre
        div.innerHTML = `
            <p><strong>${a.nom}</strong> &bull; ${a.voiture} &bull; ${a.prix} €</p>
            <p>Départ: ${a.depart}</p>
            <p>Destination: ${a.destination}</p>
            <p>Date & Heure: ${new Date(a.datetime).toLocaleString('fr-FR', {
                year: 'numeric', month: 'numeric', day: 'numeric',
                hour: '2-digit', minute: '2-digit'
            })}</p>
            <div class="actions">
                <button class="contact" onclick="contacter(${index})">Contacter</button>
                <button class="supprimer" onclick="supprimerAnnonce(${index})">Supprimer</button>
                <button class="reserver" onclick="ouvrirReservation('${a.nom}', '${a.depart}', '${a.destination}', ${index})">Réserver</button>
            </div>
        `;
        conteneur.appendChild(div);
    });
}

// Fonction pour contacter (simulée)
function contacter(index) {
    const annonces = JSON.parse(localStorage.getItem("annoncesConducteurs") || "[]");
    if (annonces[index]) {
        alert(`Vous allez contacter ${annonces[index].nom} pour le trajet de ${annonces[index].depart} à ${annonces[index].destination}. Cette fonctionnalité arrive bientôt!`);
    } else {
        alert("Annonce introuvable.");
    }
}

// Fonction pour supprimer une annonce (côté client, pour l'exemple)

function supprimerAnnonce(index) {
    if (confirm("Êtes-vous sûr de vouloir supprimer cette annonce ?")) {
        let annonces = JSON.parse(localStorage.getItem("annoncesConducteurs") || "[]");
        if (index > -1 && index < annonces.length) {
            annonces.splice(index, 1); // Supprime l'élément à l'index donné
            localStorage.setItem("annoncesConducteurs", JSON.stringify(annonces)); // Met à jour localStorage
            afficherToutesLesAnnonces(); // Rafraîchit la liste
            alert("Annonce supprimée.");
        } else {
            alert("Annonce invalide.");
        }
    }
}

// Fonction pour ouvrir la page de réservation (simulée)
function ouvrirReservation(nom, depart, destination, index) {
   
    // avec les détails de l'annonce pré-remplis, ou ouvrirait une modal.
    alert(`Fonctionnalité de réservation pour le trajet de ${nom} de ${depart} vers ${destination}.`);
    
    window.location.href = `{% url 'nom_de_votre_url_reservation' %}?nom=${encodeURIComponent(nom)}&depart=${encodeURIComponent(depart)}&destination=${encodeURIComponent(destination)}`;
}


// Appelle la fonction d'affichage lorsque la page est entièrement chargée
window.onload = afficherToutesLesAnnonces;

// Pour tester, vous pouvez ajouter quelques annonces dans localStorage manuellement via la console du navigateur:
/*
const annoncesTest = [
    {
        nom: "Jean Dupont",
        voiture: "Renault Clio",
        prix: 15,
        depart: "Cotonou",
        destination: "Abomey-Calavi",
        datetime: new Date().toISOString()
    },
    {
        nom: "Marie Curie",
        voiture: "Peugeot 308",
        prix: 20,
        depart: "Porto-Novo",
        destination: "Cotonou",
        datetime: new Date(Date.now() + 86400000).toISOString() // Demain
    }
];
localStorage.setItem("annoncesConducteurs", JSON.stringify(annoncesTest));
*/