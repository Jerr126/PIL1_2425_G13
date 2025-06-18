document.getElementById("btnConfirmerReservation").addEventListener("click", () => {
    fermerReservation();

    let reservations = JSON.parse(localStorage.getItem("reservationsPassager") || "[]");
    reservations.push(trajetSelectionne);
    localStorage.setItem("reservationsPassager", JSON.stringify(reservations));

    alert("Réservation confirmée pour le trajet de $ { trajetSelectionne.nom }!");
});