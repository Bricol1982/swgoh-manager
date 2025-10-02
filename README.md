# SWGOH Personal Manager

Application web personnelle pour la gestion et l'optimisation de votre roster Star Wars: Galaxy of Heroes (SWGOH).

## ⚠️ IMPORTANT - Usage Personnel Uniquement

Cette application est conçue pour un **usage local et personnel uniquement**. Elle ne modifie ni n'automatise rien directement dans le jeu. Toutes les optimisations et suggestions doivent être appliquées **manuellement** par le joueur dans SWGOH.

## 🌟 Fonctionnalités

### 📊 Dashboard
- Vue d'ensemble de votre roster
- Statistiques clés (GP, nombre de personnages, etc.)
- Top 10 personnages par Galactic Power
- Actions rapides vers les autres sections

### 📦 Gestionnaire de Mods
- Visualisation de tous vos mods (équipés et non équipés)
- Filtrage par vitesse, slot, rareté
- Statistiques détaillées sur vos mods
- Export en CSV pour analyse externe
- Pagination pour gérer de grands rosters

### ⚙️ Optimiseur de Mods
- Optimisation automatique basée sur vos priorités
- Presets pour différents types de personnages (Speed, Offense, Tank, Balanced)
- Pondération personnalisable des stats
- Suggestions de mods avec instructions détaillées
- Export des configurations d'optimisation

### 💾 Gestion des Loadouts
- Création et sauvegarde de configurations d'équipes
- Organisation par type d'événement (GAC, TW, TB, Raids, Conquest)
- Import/Export de loadouts au format JSON
- Gestion de plusieurs configurations pour différentes stratégies

### ⚔️ Comparaison GAC
- Comparaison de votre roster avec un adversaire
- Analyse détaillée des forces et faiblesses
- Recommandations stratégiques personnalisées
- Comparaison des top 20 personnages
- Export des analyses

## 📋 Prérequis

- Python 3.7 ou supérieur
- Un navigateur web moderne (Chrome, Firefox, Edge, Safari)
- Votre Ally Code SWGOH

## 🚀 Installation

### 1. Télécharger le projet

Créez un nouveau dossier pour le projet et placez-y tous les fichiers :

```
swgoh-manager/
├── app.py
├── README.md
├── requirements.txt
└── templates/
    ├── base.html
    ├── index.html
    ├── mods.html
    ├── optimizer.html
    ├── loadouts.html
    └── gac.html
```

### 2. Créer le fichier requirements.txt

Créez un fichier `requirements.txt` avec le contenu suivant :

```
Flask==2.3.0
requests==2.31.0
pandas==2.0.0
```

### 3. Installer les dépendances

Ouvrez un terminal/invite de commandes dans le dossier du projet et exécutez :

```bash
pip install -r requirements.txt
```

Ou installez les packages individuellement :

```bash
pip install Flask requests pandas
```

### 4. Configuration de l'API (Optionnel)

L'application utilise l'API publique de SWGOH.gg par défaut, qui ne nécessite pas de clé API. Cependant, pour de meilleures performances, vous pouvez obtenir une clé API de SWGOH.help :

1. Inscrivez-vous sur https://swgoh.help
2. Obtenez votre token API
3. Dans `app.py`, remplacez `YOUR_API_TOKEN_HERE` par votre token

**Note :** Sans token SWGOH.help, l'application utilisera SWGOH.gg ou des données de démonstration.

## 🎮 Utilisation

### Démarrer l'application

1. Ouvrez un terminal dans le dossier du projet
2. Exécutez :

```bash
python app.py
```

3. Ouvrez votre navigateur et allez à : `http://localhost:5000`

### Premier démarrage

1. **Dashboard** : Entrez votre Ally Code (format : 123-456-789)
2. Cliquez sur **"📥 Récupérer les données"**
3. Attendez que vos données soient chargées (cela peut prendre quelques secondes)
4. Explorez les différentes sections !

### Utilisation des fonctionnalités

#### Gestion des Mods
1. Allez dans la section **Mods**
2. Utilisez les filtres pour trouver des mods spécifiques
3. Cliquez sur un mod pour voir ses détails
4. Exportez vos mods en CSV pour analyse externe

#### Optimisation
1. Allez dans la section **Optimizer**
2. Sélectionnez un personnage
3. Choisissez un preset ou ajustez manuellement les poids des stats
4. Cliquez sur **"🚀 Lancer l'Optimisation"**
5. Suivez les instructions pour appliquer les changements **manuellement** dans le jeu

#### Loadouts
1. Allez dans la section **Loadouts**
2. Créez un nouveau loadout avec le bouton **"➕ Créer un Nouveau Loadout"**
3. Sélectionnez jusqu'à 5 personnages pour créer une équipe
4. Sauvegardez et gérez vos différentes configurations

#### Comparaison GAC
1. Allez dans la section **GAC Compare**
2. Entrez l'Ally Code de votre adversaire
3. Cliquez sur **"📥 Charger l'Adversaire"**
4. Lancez la comparaison pour obtenir des analyses et recommandations

## 💾 Données

### Stockage Local
Toutes vos données sont stockées localement dans une base de données SQLite (`swgoh_data.db`) dans le dossier du projet. Aucune donnée n'est envoyée à des serveurs tiers (sauf lors de la récupération initiale depuis l'API SWGOH).

### Sauvegarde
Pour sauvegarder vos données :
1. Copiez le fichier `swgoh_data.db`
2. Exportez vos loadouts individuellement

### Restauration
Pour restaurer vos données :
1. Remplacez `swgoh_data.db` par votre sauvegarde
2. Redémarrez l'application

## 🔧 Dépannage

### Erreur "Module not found"
- Assurez-vous d'avoir installé toutes les dépendances : `pip install -r requirements.txt`

### Erreur "Address already in use"
- Le port 5000 est déjà utilisé. Modifiez le port dans `app.py` :
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### Impossible de récupérer les données
- Vérifiez votre connexion Internet
- Assurez-vous que votre Ally Code est correct
- L'API SWGOH.gg peut être temporairement indisponible - réessayez plus tard

### La base de données est corrompue
- Supprimez le fichier `swgoh_data.db` et redémarrez l'application
- Vous devrez recharger vos données depuis l'API

## 📊 Structure de la Base de Données

L'application utilise SQLite avec les tables suivantes :

- **player_info** : Informations générales du joueur
- **characters** : Tous vos personnages avec stats
- **mods** : Tous vos mods (équipés et non équipés)
- **loadouts** : Vos configurations d'équipes sauvegardées
- **optimization_priorities** : Priorités d'optimisation personnalisées

## 🔐 Sécurité et Confidentialité

- ✅ Toutes les données sont stockées **localement** sur votre ordinateur
- ✅ Aucune donnée sensible n'est envoyée à des serveurs tiers
- ✅ Pas de connexion directe au jeu (aucun risque de ban)
- ✅ Votre Ally Code est le seul identifiant utilisé (information publique)
- ✅ Application prévue pour usage local uniquement (localhost)

## ⚠️ Limitations

- Pas d'interaction directe avec le jeu (toutes modifications manuelles)
- Dépend de la disponibilité des APIs publiques SWGOH
- Les données doivent être actualisées manuellement
- Optimisations basées sur des calculs locaux (peuvent différer du jeu)
- Pas de synchronisation multi-appareils

## 🛠️ Développement Futur

Fonctionnalités potentielles :
- [ ] Intégration avec Grand Ivory (optimiseur externe)
- [ ] Calculateur de statistiques avancé
- [ ] Recommandations pour événements spécifiques (TB, TW)
- [ ] Tracker de progression
- [ ] Graphiques et visualisations avancées
- [ ] Mode multi-joueurs (comparaison de guilde)

## 📝 Notes Importantes

1. **Responsabilité** : Cet outil est fourni "tel quel" sans garantie. Utilisez-le à vos propres risques.

2. **Conformité TOS** : Cette application ne viole pas les Terms of Service de SWGOH car :
   - Elle n'automatise rien dans le jeu
   - Elle n'utilise que des APIs publiques
   - Toutes les actions doivent être effectuées manuellement par le joueur

3. **Mises à jour** : Les APIs SWGOH peuvent changer. Cette application peut nécessiter des mises à jour pour continuer à fonctionner.

## 🤝 Contributions

Ce projet est open-source pour usage personnel. N'hésitez pas à le modifier selon vos besoins !

## 📄 Licence

Usage personnel uniquement. Ne pas distribuer ou utiliser à des fins commerciales.

## 📧 Support

Pour des questions ou problèmes :
1. Vérifiez la section Dépannage ci-dessus
2. Consultez les logs dans la console du terminal
3. Vérifiez la console du navigateur (F12) pour les erreurs JavaScript

## 🎯 Exemples d'Utilisation

### Scénario 1 : Préparation GAC
1. Chargez votre roster depuis le Dashboard
2. Allez dans GAC Compare et chargez votre adversaire
3. Analysez les recommandations stratégiques
4. Créez des loadouts pour chaque zone de défense
5. Utilisez l'optimiseur pour maximiser vos personnages clés

### Scénario 2 : Optimisation de Roster
1. Allez dans Mods et filtrez les mods non équipés
2. Identifiez vos meilleurs mods (vitesse +20)
3. Utilisez l'optimiseur pour suggérer de nouveaux équipements
4. Appliquez manuellement dans le jeu
5. Re-synchronisez pour vérifier

### Scénario 3 : Gestion d'Événement TB
1. Créez un loadout "TB Light Side Phase 1"
2. Sélectionnez vos 5 meilleurs Jedi
3. Sauvegardez la configuration
4. Répétez pour chaque phase
5. Consultez vos loadouts avant chaque phase

## 📚 Ressources Utiles

- **SWGOH.gg** : https://swgoh.gg - Base de données officielle
- **SWGOH.help** : https://api.swgoh.help - Documentation API
- **Grand Ivory** : https://www.grandivory.com - Optimiseur de mods externe
- **Discord SWGOH** : Communauté active pour support

## 🔄 Mise à Jour de l'Application

Pour mettre à jour vers une nouvelle version :

1. **Sauvegardez vos données** :
   ```bash
   cp swgoh_data.db swgoh_data.db.backup
   ```

2. **Remplacez les fichiers** : Téléchargez et remplacez `app.py` et les templates

3. **Redémarrez l'application** :
   ```bash
   python app.py
   ```

## 🎨 Personnalisation

### Modifier les Couleurs
Éditez `templates/base.html` dans la section `<style>` pour changer les couleurs de l'interface.

### Ajouter des Presets d'Optimisation
Dans `templates/optimizer.html`, modifiez l'objet `presets` :
```javascript
const presets = {
    speed: { speed: 2.0, offense: 0.3, protection: 0.2, health: 0.2 },
    // Ajoutez vos presets personnalisés ici
};
```

### Modifier le Port du Serveur
Dans `app.py`, ligne finale :
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Changez 5000
```

## 🐛 Signalement de Bugs

Si vous rencontrez un bug :

1. **Vérifiez les logs du serveur** dans le terminal
2. **Vérifiez la console du navigateur** (F12 → Console)
3. **Notez les étapes** pour reproduire le bug
4. **Vérifiez votre version** de Python et des dépendances

### Logs Utiles

Le serveur affiche des logs détaillés :
```
Erreur API: [détails de l'erreur]
Erreur sauvegarde: [détails de l'erreur]
```

Pour activer plus de logs, modifiez dans `app.py` :
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 💡 Conseils et Astuces

### Performance
- **Actualisation** : Actualisez vos données tous les 2-3 jours pour rester à jour
- **Filtrage** : Utilisez les filtres pour accélérer la recherche de mods
- **Pagination** : Pour les grands rosters, utilisez la pagination (50 items par page)

### Optimisation
- **Presets** : Commencez avec les presets avant de personnaliser
- **Vitesse** : Pour la plupart des personnages GAC, priorisez la vitesse
- **Contexts** : Ajustez les poids selon le contexte (Raids vs GAC)

### Loadouts
- **Organisation** : Nommez vos loadouts clairement (ex: "GAC Def Zone 1 - JKR Lead")
- **Descriptions** : Ajoutez des notes stratégiques dans la description
- **Export** : Exportez vos loadouts avant un événement majeur

### Comparaison GAC
- **Anticipation** : Chargez votre adversaire dès que possible
- **Analyse** : Lisez attentivement les recommandations stratégiques
- **Flexibilité** : Préparez des plans A, B et C

## 🔍 FAQ

**Q: L'application est-elle sûre ? Vais-je être banni ?**  
R: Oui, elle est sûre. Elle n'interagit pas directement avec le jeu et utilise uniquement des APIs publiques. Toutes les modifications sont manuelles.

**Q: Puis-je utiliser cette application sur mobile ?**  
R: L'interface est responsive, mais pour la meilleure expérience, utilisez un ordinateur. Vous pouvez accéder à l'application depuis un mobile si votre ordinateur est sur le même réseau (remplacez localhost par l'IP locale).

**Q: Les optimisations sont-elles précises ?**  
R: Les optimisations sont basées sur des calculs locaux et peuvent différer légèrement du jeu. Utilisez-les comme guide, pas comme vérité absolue.

**Q: Puis-je partager mes loadouts avec ma guilde ?**  
R: Oui ! Utilisez la fonction d'export JSON et partagez le fichier. Vos coéquipiers peuvent l'importer.

**Q: L'application fonctionne-t-elle hors ligne ?**  
R: Une fois les données chargées, vous pouvez utiliser la plupart des fonctionnalités hors ligne (optimisation, loadouts). Seule la récupération de données nécessite Internet.

**Q: Combien de temps prend la synchronisation ?**  
R: Entre 5 et 30 secondes selon la taille de votre roster et la vitesse de l'API.

**Q: Puis-je gérer plusieurs comptes ?**  
R: Oui ! Changez simplement l'Ally Code dans le Dashboard. Les données de chaque compte sont stockées séparément.

**Q: Les mods non équipés sont-ils inclus ?**  
R: Oui, tous vos mods sont récupérés, équipés ou non. Utilisez les filtres pour les distinguer.

## 🏗️ Architecture Technique

### Backend (Flask)
- **Framework** : Flask 2.3.0
- **Base de données** : SQLite3 (inclus avec Python)
- **API** : Requests pour les appels HTTP

### Frontend
- **HTML/CSS** : Interface responsive moderne
- **JavaScript** : Vanilla JS (pas de framework lourd)
- **Design** : Dark theme optimisé pour les longues sessions

### Flux de Données
```
API SWGOH.gg → Flask → SQLite → Flask → Frontend → Utilisateur
                ↓
         Optimisations locales
                ↓
         Suggestions affichées
```

## 🧪 Tests

Pour tester l'application :

1. **Test de base** :
   ```bash
   python app.py
   ```
   Vérifiez que le serveur démarre sans erreur

2. **Test avec données de démo** :
   - Si l'API échoue, des données de démo sont générées automatiquement
   - Utilisez l'Ally Code `123456789` pour tester

3. **Test d'optimisation** :
   - Chargez un personnage
   - Lancez une optimisation
   - Vérifiez que les résultats s'affichent

## 📦 Déploiement (Optionnel)

Si vous souhaitez accéder à l'application depuis d'autres appareils sur votre réseau local :

1. **Trouvez votre IP locale** :
   - Windows : `ipconfig`
   - Mac/Linux : `ifconfig` ou `ip addr`

2. **Démarrez avec l'IP** :
   L'application écoute déjà sur `0.0.0.0`, donc elle est accessible depuis n'importe quel appareil du réseau.

3. **Accédez depuis un autre appareil** :
   ```
   http://[VOTRE_IP_LOCALE]:5000
   ```
   Exemple : `http://192.168.1.100:5000`

**⚠️ Ne déployez JAMAIS cette application sur Internet public !**

## 🎓 Apprentissage

Ce projet peut servir d'exemple pour apprendre :
- **Flask** : Application web Python basique
- **SQLite** : Gestion de base de données
- **API REST** : Consommation d'APIs tierces
- **Frontend** : HTML/CSS/JS moderne
- **Architecture MVC** : Séparation des responsabilités

## 🌟 Crédits

- **CG (Capital Games)** : Pour Star Wars: Galaxy of Heroes
- **SWGOH.gg** : Pour l'API publique
- **Communauté SWGOH** : Pour les outils et le support

---

**Version** : 1.0.0  
**Dernière mise à jour** : 2025  
**Auteur** : Usage Personnel

**May the Force be with you!** ⚔️✨