# Gestion des Données — ARTEMIS_EARTH_DETECTIVE

Ce répertoire structure le cycle de traitement des données scientifiques de la NASA au sein de l'application :

* `raw/` : Jeux de données bruts originaux importés depuis les portails de la NASA (ex. `zone_interet.geojson`).
* `cache/` : Fichiers intermédiaires mis en mémoire pour accélérer les analyses et les requêtes spatiales.
* `exports/` : Jeux de données nettoyés et structurés prêts pour l'intégration PostGIS sur Supabase ou le téléchargement.
*