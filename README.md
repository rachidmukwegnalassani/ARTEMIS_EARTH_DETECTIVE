# ARTEMIS_EARTH_DETECTIVE

**ARTEMIS_EARTH_DETECTIVE** est un module de l'application Web **ARTEMIS GEOMATIC IA**, conçu spécialement pour relever le défi du **NASA Space Apps Challenge** : *"Be an Earth System Detective"* (*Soyez un détective des tendances du système Terre*).

##  Accès à la plateforme (Parcours complet)
1. **Site Vitrine & Présentation (Frontend) :** [https://artemisearthdetective-frontend.vercel.app/](https://artemisearthdetective-frontend.vercel.app/)
2. **Tableau de bord & Moteur d'analyse (App/Backend) :** [https://artemis-earth-detective.onrender.com/](https://artemis-earth-detective.onrender.com/)

## Fonctionnalités principales
* **Chargement multi-formats :** Import et analyse de données géospatiales (`.geojson`, `.shp`, `.tif`, `.nc`, `.hdf`), graphiques, statistiques (`.csv`, `.xlsx`) et documents scientifiques (`.pdf`, `.txt`).
* **Base de données spatiale :** Stockage et requêtes géographiques propulsés par PostgreSQL et l'extension **PostGIS** sur **Supabase**.
* **Assistant IA Artemis :** Analyse automatisée et chat interactif pour explorer les tendances environnementales et climatiques.

##  Architecture & Technologies
* **Site Vitrine :** HTML5, CSS3, JavaScript (hébergé sur **Vercel**).
* **Application & API :** Python 3.12, FastAPI, Uvicorn (hébergés sur **Render**).
* **Base de données :** PostgreSQL + PostGIS (hébergés sur **Supabase**).
* **Gestion des dépendances :** `pyproject.toml` & `uv`.

## Structure du projet
* `frontend/` : Site-vitrine et interface utilisateur (`app-dashboard`).
* `backend/` : API FastAPI, logique d'analyse et utilitaires géospatiaux.
* `docs/` : Documentation technique et architecture du système.
* `tests/` : Tests automatisés de l'API et des modules.
* `deployment/` : Notes et configurations de déploiement.

##  Installation locale
1. Cloner le dépôt : `git clone https://github.com/rachidmukwegnalassani/ARTEMIS_EARTH_DETECTIVE`
2. Installer les dépendances : `uv sync` (ou `pip install -e .`)
3. Configurer les variables d'environnement dans un fichier `.env` (`DATABASE_URL`, clés API).
4. Lancer le serveur : `uvicorn backend.main:app --reload`
