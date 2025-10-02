# 📁 Structure du Projet - SWGOH Personal Manager

## Arborescence Complète

```
swgoh-manager/
│
├── 📄 app.py                    # Application Flask principale (backend)
├── 📄 requirements.txt          # Dépendances Python
├── 📄 README.md                 # Documentation complète
├── 📄 QUICKSTART.md             # Guide de démarrage rapide
├── 📄 STRUCTURE.md              # Ce fichier - structure du projet
├── 📄 .gitignore                # Fichiers à ignorer (git)
│
├── 🚀 start.bat                 # Script de démarrage Windows
├── 🚀 start.sh                  # Script de démarrage Mac/Linux
│
├── 💾 swgoh_data.db             # Base de données SQLite (créée au 1er lancement)
│
└── 📁 templates/                # Templates HTML (frontend)
    ├── base.html                # Template de base (layout commun)
    ├── index.html               # Page Dashboard
    ├── mods.html                # Page Gestion des Mods
    ├── optimizer.html           # Page Optimiseur
    ├── loadouts.html            # Page Loadouts
    └── gac.html                 # Page Comparaison GAC
```

## 📝 Description des Fichiers

### Backend (Python/Flask)

#### `app.py` (~ 500 lignes)
**Rôle** : Cœur de l'application, gère toute la logique serveur

**Sections principales** :
- Configuration Flask et variables globales
- `init_db()` : Initialisation de la base de données SQLite
- `fetch_player_data()` : Récupération des données via API SWGOH
- `save_player_data()` : Sauvegarde des données en base
- `optimize_mods_for_character()` : Algorithme d'optimisation des mods
- Routes Flask (`@app.route`) :
  - `/` : Page d'accueil
  - `/mods`, `/optimizer`, `/loadouts`, `/gac` : Pages principales
  - `/api/*` : Endpoints API (JSON)

**APIs principales** :
- `POST /api/fetch_player` : Récupère les données d'un joueur
- `GET /api/player_info/<ally_code>` : Info joueur depuis DB
- `GET /api/characters/<ally_code>` : Liste des personnages
- `GET /api/mods/<ally_code>` : Liste des mods
- `POST /api/optimize` : Optimisation de mods
- `POST /api/loadout/save` : Sauvegarde d'un loadout
- `GET /api/loadouts/<ally_code>` : Liste des loadouts
- `GET /api/export/mods/<ally_code>` : Export CSV
- `POST /api/compare` : Comparaison de joueurs

**Technologies** :
- Flask : Framework web
- SQLite3 : Base de données
- Requests : Appels API HTTP
- Pandas : Manipulation de données

### Frontend (HTML/CSS/JavaScript)

#### `templates/base.html` (~ 400 lignes)
**Rôle** : Template parent, définit le layout commun à toutes les pages

**Contient** :
- `<head>` : Meta tags, CSS global
- Navigation : Barre de menu responsive
- Styles CSS : Variables, classes réutilisables, animations
- Scripts JavaScript globaux : Helpers, localStorage, alertes
- Blocks Jinja2 : `{% block content %}`, `{% block extra_scripts %}`

**Design** :
- Dark theme (fond dégradé noir/bleu)
- Couleur primaire : Or (#ffd700)
- Glassmorphism : backdrop-filter, transparence
- Responsive : Grid CSS, flex, media queries

#### `templates/index.html` (~ 300 lignes)
**Rôle** : Dashboard principal, première page vue par l'utilisateur

**Sections** :
1. Formulaire Ally Code + boutons fetch/refresh
2. Infos joueur : GP, niveau, nombre de personnages
3. Statistiques en grid : GP total, chars, ships
4. Top 10 personnages par GP (tableau)
5. Actions rapides : Boutons vers autres sections

**JavaScript** :
- `fetchPlayerData()` : Appel API pour charger le roster
- `loadPlayerInfo()` : Charge depuis DB locale
- `loadTopCharacters()` : Affiche top personnages
- localStorage pour mémoriser l'Ally Code

#### `templates/mods.html` (~ 400 lignes)
**Rôle** : Gestionnaire de mods complet

**Fonctionnalités** :
1. Boutons de filtrage : Tous / Équipés / Non équipés
2. Statistiques : Total, équipés, non équipés, vitesse +15
3. Filtres avancés : Vitesse min, slot, rareté
4. Tableau paginé (50 mods/page)
5. Modal détails mod (clic sur une ligne)
6. Export CSV

**JavaScript** :
- `loadMods()` : Charge depuis API
- `applyFilters()` : Filtre local
- `displayMods()` : Affichage paginé
- `showModDetails()` : Modal popup
- Pagination dynamique

#### `templates/optimizer.html` (~ 450 lignes)
**Rôle** : Optimiseur de mods intelligent

**Workflow** :
1. Sélection personnage (dropdown)
2.