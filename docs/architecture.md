# Architecture Technique — ARTEMIS_EARTH_DETECTIVE

**ARTEMIS_EARTH_DETECTIVE** est conçu selon une architecture modulaire découplant l'interface utilisateur, le traitement scientifique des données et le stockage géospatial.

## 1. Flux de données et fonctionnement

1. **Portail Vitrine (Frontend) :** Hébergé sur **Vercel**, il présente la solution et redirige l'utilisateur vers le tableau de bord.
2. **Tableau de bord interactif (`app-dashboard`) :** Permet d'importer des fichiers scientifiques (`.geojson`, `.shp`, `.tif`, `.nc`, `.hdf`, `.csv`, `.xlsx`, `.pdf`) et d'interroger l'assistant IA Artemis.
3. **Moteur Backend & API (FastAPI sur Render) :**
   * **Parsers :** Extraction et validation des structures géospatiales et tabulaires.
   * **Engines :** Calculs statistiques et analyse des variables environnementales de la NASA.
   * **Assistant IA Artemis :** Analyse contextuelle des données chargées et réponses scientifiques en langage naturel.
4. **Base de données spatiale (Supabase) :** Stockage persistant des entités géographiques via **PostgreSQL + PostGIS**.

## 2. Organisation du dépôt

* `frontend/` : Site vitrine et interface du tableau de bord (`app-dashboard`).
* `backend/` : API FastAPI, logique métier, parseurs, utilitaires géospatiaux et zone de transit (`temp-uploads/`).
* `data/` : Cycle de vie des données (`raw/`, `cache/`, `exports/`).
* `notebooks/` : Carnet de validation scientifique (`01-test-parsers.ipynb`).
* `tests/` : Tests automatisés (`pytest`) validant l'API, les parseurs, les calculs et le chat.
* `reports/` : Livrables exportés (`HTML/`, `images/`, `PDF/`).
* `deployment/` : Documentation de mise en production.
