let currentMode = 'passenger'; // Valeur par défaut

function setActiveButton() {
    document.getElementById('passengerBtn').classList.toggle('active', currentMode === 'passenger');
    document.getElementById('driverBtn').classList.toggle('active', currentMode === 'driver');
}

function fetchNotifications() {
    fetch(`/api/notifications/?mode=${currentMode}`)
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('notificationsList');
            list.innerHTML = '';
            if (data.length === 0) {
                list.innerHTML = '<p>Aucune notification.</p>';
            } else {
                data.forEach(notif => {
                    const div = document.createElement('div');
                    div.className = 'notification';
                    div.textContent = notif.message;
                    list.appendChild(div);
                });
            }
        });
}
document.getElementById('passengerBtn').onclick = () => {
    currentMode = 'passenger';
    setActiveButton();
    fetchNotifications();
};
document.getElementById('driverBtn').onclick = () => {
    currentMode = 'driver';
    setActiveButton();
    fetchNotifications();
};

// Initialisation
setActiveButton();
fetchNotifications();