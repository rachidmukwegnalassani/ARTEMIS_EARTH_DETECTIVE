document.addEventListener("DOMContentLoaded", () => {
  const boutonAcceder = document.getElementById("btn-acceder-app");

  if (boutonAcceder) {
    boutonAcceder.addEventListener("click", async (event) => {
      event.preventDefault();
      boutonAcceder.textContent = "Réveil du moteur Artemis...";

      try {
        await fetch("https://artemis-earth-detective.onrender.com");
      } catch (error) {
        console.warn("Démarrage du serveur en cours...", error);
      } finally {
        window.location.href = "https://artemis-earth-detective.onrender.com";
      }
    });
  }
});