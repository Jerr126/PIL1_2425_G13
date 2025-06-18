document.addEventListener('DOMContentLoaded', () => {
  // Sélection des éléments décoratifs
  const decorElements = document.querySelectorAll('.decor');

  // Fonction pour générer un délai aléatoire
  const getRandomDelay = () => Math.random() * 2 + 1;

  // Fonction pour générer une échelle aléatoire
  const getRandomScale = () => 0.9 + Math.random() * 0.2;

  // Animation pour chaque élément décoratif
  decorElements.forEach(element => {
    const isSun = element.classList.contains('decor-sun');
    const isPlane = element.classList.contains('decor-plane');
    
    // Animation de pulsation pour le soleil
    if (isSun) {
      element.animate(
        [
          { transform: 'scale(1)', opacity: 0.25 },
          { transform: `scale(${getRandomScale()})`, opacity: 0.4 },
          { transform: 'scale(1)', opacity: 0.25 }
        ],
        {
          duration: 5000,
          iterations: Infinity,
          easing: 'ease-in-out',
          delay: getRandomDelay() * 1000
        }
      );
    }
    
    // Animation de rotation pour l'avion
    if (isPlane) {
      element.animate(
        [
          { transform: 'rotate(0deg)' },
          { transform: 'rotate(5deg)' },
          { transform: 'rotate(0deg)' }
        ],
        {
          duration: 3000,
          iterations: Infinity,
          easing: 'ease-in-out',
          delay: getRandomDelay() * 1000
        }
      );
    }

    // Animation de flottement aléatoire pour les nuages, voiture et moto
    if (!isSun && !isPlane) {
      element.animate(
        [
          { transform: 'translateY(0px)' },
          { transform: `translateY(${Math.random() * 20 - 10}px)` },
          { transform: 'translateY(0px)' }
        ],
        {
          duration: 4000,
          iterations: Infinity,
          easing: 'ease-in-out',
          delay: getRandomDelay() * 1000
        }
      );
    }
  });

  // Animation au survol pour les icônes décoratives
  decorElements.forEach(element => {
    element.addEventListener('mouseenter', () => {
      element.animate(
        [
          { transform: 'scale(1)' },
          { transform: 'scale(1.2)' },
          { transform: 'scale(1)' }
        ],
        {
          duration: 500,
          easing: 'ease-out'
        }
      );
    });
  });
});
