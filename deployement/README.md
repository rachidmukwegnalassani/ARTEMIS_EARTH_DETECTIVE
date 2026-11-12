# Guide de Déploiement — ARTEMIS_EARTH_DETECTIVE

L'architecture de **ARTEMIS_EARTH_DETECTIVE** repose sur un déploiement cloud distribué en trois briques interconnectées. Chaque composant est synchronisé automatiquement avec le dépôt GitHub principal.

## 1. Architecture Cloud en Production

* **Site Vitrine (Frontend) :** Hébergé sur **Vercel** ([https://artemisearthdetective-frontend.vercel.app](https://vercel.app)). Il présente le projet et redirige l'utilisateur vers l'application d'analyse.
* **Tableau de bord & API (Backend) :** Hébergés sur **Render** ([https://artemis-earth-detective.onrender.com](https://://onrender.com/)). Le serveur tourne sous Python 3.12 avec FastAPI et Uvicorn.
* **Base de données spatiale :** Hébergée sur **Supabase** avec PostgreSQL et l'extension géographique **PostGIS** activée.

## 2. Configuration du Serveur Render

* **Environnement :** Python 3.12
* **Gestionnaire de paquets :** `pyproject.toml` / `uv`
* **Commande de démarrage :**
  ```bash
  uvicorn backend.main:app --host 0.0.0.0 --port \$PORT
  ```
* **Variables d'environnement requises (configurées dans le tableau de bord Render) :**
  * `DATABASE_URL` : Chaîne de connexion PostgreSQL fournie par Supabase.
  * Clés API nécessaires aux services d'analyse et au chat Artemis.

## 3. Exécution via Docker (Optionnel)

Pour tester le conteneur backend en local tout en restant connecté à la base de données Supabase :

1. Créer un fichier `.env` à la racine du projet contenant la variable `DATABASE_URL`.
2. Lancer le service avec Docker Compose :
   ```bash
   docker-compose up --build
   ```