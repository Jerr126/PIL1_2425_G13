// Mode utilisateur
    let userMode = "passenger";
    let userName = "Marie";
    let publishedRides = [];
    
    // Éléments du DOM
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const menuSpace = document.getElementById('menuSpace');
    
    // Gestion du menu mobile
    mobileMenuBtn.addEventListener('click', toggleMenu);
    
    // Fermer le menu en cliquant à l'extérieur
    document.addEventListener('click', (e) => {
      if (!menuSpace.contains(e.target) && e.target !== mobileMenuBtn) {
        closeMenu();
      }
    });
    
    function toggleMenu() {
      menuSpace.classList.toggle('active');
    }
    
    function closeMenu() {
      menuSpace.classList.remove('active');
    }
    
    // Gestion des popups
    function handleSearch() {
      showPopup('searchPopup');
      // Pré-remplir la date du jour
      const today = new Date().toISOString().split('T')[0];
      document.getElementById('date').value = today;
      // Pré-remplir l'heure actuelle + 1h
      const now = new Date();
      now.setHours(now.getHours() + 1);
      document.getElementById('time').value = now.toTimeString().substring(0, 5);
    }
    
   
    
    function handlePublish() {
      if (userMode === "passenger") {
        showPopup('popup'); 
      } else {
        showPublishPopup(); // Popup pour publier un trajet
      }
    }

    function showPublishPopup() {
      // Pré-remplir la date et l'heure
      const today = new Date().toISOString().split('T')[0];
      document.getElementById('publishDate').value = today;
      
      const now = new Date();
      now.setHours(now.getHours() + 1);
      document.getElementById('publishTime').value = now.toTimeString().substring(0, 5);
      
      showPopup('publishPopup');
    }

    function closePublishPopup() {
      document.getElementById('publishPopup').style.display = "none";
      document.body.style.overflow = "auto";
    }

    function closePublishSuccessPopup() {
      document.getElementById('publishSuccessPopup').style.display = "none";
      document.body.style.overflow = "auto";
    }

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
      
      // Création du trajet
      const newRide = {
        id: Date.now(),
        driver: userName,
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
      
      // Ajout aux trajets publiés
      publishedRides.unshift(newRide);
      console.log('Trajet publié :', newRide);
      
      // Sauvegarde dans le localStorage
      saveRidesToLocalStorage();
      
      // Fermer le popup et afficher la confirmation
      closePublishPopup();
      showPopup('publishSuccessPopup');
    }

    function saveRidesToLocalStorage() {
      localStorage.setItem('publishedRides', JSON.stringify(publishedRides));
    }

    function loadRidesFromLocalStorage() {
      const rides = localStorage.getItem('publishedRides');
      if (rides) {
        publishedRides = JSON.parse(rides);
      }
    }

    // Au chargement de la page
    document.addEventListener('DOMContentLoaded', () => {
      animateElements();
      loadRidesFromLocalStorage();
      
      setTimeout(() => {
        document.querySelector('.search-bar input').placeholder = `${userName}, où souhaitez-vous aller aujourd'hui ?`;
      }, 1000);
    });
    
    function showPopup(id) {
      document.getElementById(id).style.display = "flex";
      document.body.style.overflow = "hidden";
    }
    
    function closePopup() {
      document.getElementById('popup').style.display = "none";
      document.body.style.overflow = "auto";
    }
    
    function closeSearchPopup() {
      document.getElementById('searchPopup').style.display = "none";
      document.body.style.overflow = "auto";
    }
    
    function redirectToProfile() {
      sessionStorage.setItem('redirectAfterProfile', 'publish.html');
      window.location.href = "profile.html";
    }
    
    // Recherche de trajet
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
      
      // Formatage des données
      const searchData = {
        from: departure,
        to: arrival,
        date: formatDate(date),
        time: time,
       
        seats: passengers
      };
      
      console.log('Recherche lancée :', searchData);
      closeSearchPopup();
      
      // Simulation de recherche
      showAlert(`Recherche effectuée :\nDe ${searchData.from} à ${searchData.to}\nLe ${searchData.date} à ${searchData.time}\nDurée : ${searchData.duration}\nPlaces : ${searchData.seats}`);
    }
    
    function formatDate(dateString) {
      const options = { weekday: 'long', day: 'numeric', month: 'long' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    }
    
    function showAlert(message) {
      alert(message);
    }
    
    // Animation au chargement
    document.addEventListener('DOMContentLoaded', () => {
      animateElements();
      
      // Simuler un temps de chargement
      setTimeout(() => {
        document.querySelector('.search-bar input').placeholder = `${userName}, où souhaitez-vous aller aujourd'hui ?`;
      }, 1000);
    });
    
    function animateElements() {
      const elements = document.querySelectorAll('.search-bar, .map-container, .main-buttons, .feature-card');
      
      elements.forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.animation = `fadeInUp 0.5s ease-out ${i * 0.1}s forwards`;
      });
      
      // Ajout du CSS pour l'animation
      const style = document.createElement('style');
      style.textContent = `
        @keyframes fadeInUp {
          to { opacity: 1; transform: translateY(0); }
        }
      `;
      document.head.appendChild(style);
 }