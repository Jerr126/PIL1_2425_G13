document.addEventListener('DOMContentLoaded', function() {
    // ----------------------------------------------------
    // 1. Gestion de la photo de profil
    // L'input file a maintenant l'ID 'id_profile_picture' généré par Django.
    const fileInput = document.getElementById('id_profile_picture');
    const avatar = document.getElementById('avatar'); // L'img tag qui affiche la photo

    // La fonction est maintenant un événement listener direct sur l'input file.
    // L'appel dans le HTML devrait être 'onclick="document.getElementById('id_profile_picture').click()"'
    // et l'input lui-même aura 'onchange="handleProfilePictureChange(event)"'.
    // J'ai renommé la fonction pour éviter les conflits si elle était globale.
    window.handleProfilePictureChange = function(event) {
        const file = event.target.files[0]; // Accéder au fichier via event.target.files

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                avatar.src = e.target.result; // Met à jour l'aperçu de l'image
            };
            reader.readAsDataURL(file); // Lit le fichier comme une URL de données
        }
    };

    // ----------------------------------------------------
    // 2. Gestion du toggle Passager/Conducteur et des champs associés
    // La checkbox du toggle est maintenant 'id_is_conducteur'.
    const roleToggle = document.getElementById('id_is_conducteur');
    // Le conteneur des champs spécifiques au véhicule est '.vehicle-info-section'.
    const vehicleInfoSection = document.querySelector('.vehicle-info-section');

    // Références aux champs spécifiques au conducteur pour les rendre obligatoires/non-obligatoires
    const typeVehiculeInput = document.getElementById('id_type_vehicule');
    const matriculeInput = document.getElementById('id_matricule');
    const positionInput = document.getElementById('id_position');

    function updateVehicleFieldsVisibility() {
        if (roleToggle.checked) { // Si la case "Conducteur" est cochée
            vehicleInfoSection.style.display = 'grid'; // Afficher la section (selon votre CSS .form-grid)
            // Rendre les champs obligatoires pour la validation HTML5 côté client
            if (typeVehiculeInput) typeVehiculeInput.setAttribute('required', 'required');
            if (matriculeInput) matriculeInput.setAttribute('required', 'required');
            if (positionInput) positionInput.setAttribute('required', 'required');
        } else { // Si la case "Conducteur" n'est PAS cochée (donc, implicitement Passager)
            vehicleInfoSection.style.display = 'none'; // Cacher la section
            // Retirer l'attribut 'required' et effacer les valeurs des champs
            if (typeVehiculeInput) {
                typeVehiculeInput.removeAttribute('required');
                typeVehiculeInput.value = '';
            }
            if (matriculeInput) {
                matriculeInput.removeAttribute('required');
                matriculeInput.value = '';
            }
            if (positionInput) {
                positionInput.removeAttribute('required');
                positionInput.value = '';
            }
        }
    }

    // Exécuter la fonction au chargement initial de la page pour définir l'état correct
    updateVehicleFieldsVisibility();

    // Ajouter l'écouteur d'événements pour le changement du toggle
    roleToggle.addEventListener('change', updateVehicleFieldsVisibility);
    // ----------------------------------------------------
    // 3. Gestion des champs modifiables (avec l'emoji crayon)
    // Cette partie est pour rendre les inputs éditables/non éditables.
    // L'emoji-edit doit être positionné par rapport à son parent (le div de l'input).
    document.querySelectorAll('.emoji-edit').forEach(emoji => {
        emoji.addEventListener('click', function() {
            const input = this.previousElementSibling; // L'input est l'élément précédent
            if (input) {
                const isReadOnly = input.readOnly;
                input.readOnly = !isReadOnly; // Inverse l'état readOnly

                // Change l'emoji et le titre
                if (input.readOnly) {
                    this.textContent = '🖍'; // Crayon quand non modifiable
                    this.title = 'Modifier';
                    // Ici, si le champ était édité et est maintenant readOnly,
                    // vous pourriez déclencher une sauvegarde via AJAX si vous ne voulez pas soumettre tout le formulaire.
                    // Pour l'instant, on se base sur le bouton "Sauvegarder" du formulaire.
                } else {
                    input.focus(); // Met le focus sur le champ pour l'édition
                    this.textContent = '💾'; // Disque de sauvegarde quand modifiable
                    this.title = 'Enregistrer les modifications';
                }
            }
        });
    });
});