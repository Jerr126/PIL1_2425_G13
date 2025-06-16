function changeProfilePicture() {
    const fileInput = document.getElementById('fileInput');
    const avatar = document.getElementById('avatar');

    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            avatar.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
}
const toggle = document.getElementById('roleToggle');

toggle.addEventListener('change', function() {
    const role = toggle.checked ? "Conducteur" : "Passager";
    console.log("Rôle sélectionné :", role);
});
document.addEventListener("DOMContentLoaded", function() {
    const toggle = document.getElementById("roleToggle");
    const vehicleFields = document.querySelectorAll(".vehicle-info");

    function updateFields() {
        if (toggle.checked) {
            // Conducteur → on affiche
            vehicleFields.forEach(el => el.style.display = "block");
        } else {
            // Passager → on cache
            vehicleFields.forEach(el => el.style.display = "none");
        }
    }

    toggle.addEventListener("change", updateFields);

    // Mettre à jour dès le chargement de la page
    updateFields();
});