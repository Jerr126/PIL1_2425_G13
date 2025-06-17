const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

// Ajoute la classe 'sign-up-mode' au conteneur lorsque le bouton 'S'inscrire' est cliqué
sign_up_btn.addEventListener("click", () => {
    container.classList.add("sign-up-mode");
});

// Retire la classe 'sign-up-mode' du conteneur lorsque le bouton 'Se connecter' est cliqué
sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
});