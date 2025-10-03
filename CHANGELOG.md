# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

## [1.0.0] - 2024-10-02

### ✨ Ajouté
- **Dashboard complet** avec statistiques du roster
  - Affichage du Galactic Power total
  - Compteur de personnages et reliques R5+
  - Top 10 des personnages par GP
  - Actions rapides vers les autres pages

- **Gestionnaire de Mods**
  - Visualisation de tous les mods (équipés/non équipés)
  - Filtres avancés (vitesse minimum, slot, rareté)
  - Pagination pour grandes collections
  - Détails complets de chaque mod
  - Export en CSV

- **Optimiseur de Mods**
  - Optimisation personnalisée par personnage
  - Presets d'optimisation (Speed, Offense, Tank, Balanced)
  - Poids configurables pour chaque stat
  - Suggestions de mods avec instructions d'application
  - Comparaison avant/après
  - Export de configuration

- **Gestion des Loadouts**
  - Création de compositions d'équipes personnalisées
  - Organisation par type d'événement (GAC, TW, TB, Raids, Conquest)
  - Sauvegarde jusqu'à 5 personnages par loadout
  - Import/Export de loadouts en JSON
  - Visualisation détaillée des loadouts

- **Comparaison GAC**
  - Comparaison complète de deux rosters
  - Statistiques détaillées (total personnages, gear moyen, reliques moyennes, top 10 GP)
  - Analyse stratégique automatique
  - Recommandations tactiques
  - Export des résultats

### 🎨 Interface
- Design moderne avec glassmorphism
- Thème sombre optimisé pour les yeux
- Animations fluides et interactions réactives
- Navigation intuitive avec navbar sticky
- Modals pour les détails et formulaires
- Cartes statistiques visuelles
- Responsive design (desktop/mobile)

### 🔧 Technique
- Backend Flask avec SQLite
- API REST complète
- Gestion automatique de la base de données
- Mode démonstration si API indisponible
- Stockage local de l'Ally Code
- Gestion d'erreurs robuste
- Logs détaillés

### 📦 Infrastructure
- Script de lancement automatique (Windows/Linux/Mac)
- Configuration via fichier .env
- Tests automatisés de vérification
- Documentation complète (README, INSTALLATION)
- Fichier .gitignore configuré

### 🔒 Sécurité
- Usage local uniquement
- Données stockées localement
- Pas d'interaction directe avec le jeu
- Lecture seule des données publiques

### 📝 Documentation
- README.md complet avec guide d'utilisation
- INSTALLATION.md avec instructions détaillées
- Guide de dépannage
- Commentaires dans le code
- Avertissements légaux

## [À venir] - Prochaines versions

### 🚀 Fonctionnalités prévues
- Import de mods depuis fichiers
- Comparaison de loadouts multiples
- Historique des optimisations
- Statistiques de progression
- Suggestions de farming
- Calculateur de resources
- Mode hors ligne complet
- Thèmes personnalisables
- Export PDF des rapports
- Notifications de mise à jour

### 🐛 Corrections prévues
- Amélioration de la gestion des erreurs API
- Optimisation des performances pour grands rosters
- Cache des requêtes API
- Meilleure gestion des timeouts

### 💡 Améliorations prévues
- Interface de comparaison de mods côte à côte
- Graphiques de progression
- Suggestions basées sur les méta teams
- Intégration avec d'autres sources de données SWGOH

---

## Format du Changelog

Ce changelog suit les conventions de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

### Types de changements
- **Ajouté** : nouvelles fonctionnalités
- **Modifié** : changements de fonctionnalités existantes
- **Déprécié** : fonctionnalités bientôt supprimées
- **Supprimé** : fonctionnalités supprimées
- **Corrigé** : corrections de bugs
- **Sécurité** : corrections de vulnérabilités