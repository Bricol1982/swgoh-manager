# 🚀 Guide de Démarrage Rapide - SWGOH Personal Manager

## Installation en 3 minutes

### Étape 1 : Vérifier Python
Ouvrez un terminal et tapez :
```bash
python --version
```
ou
```bash
python3 --version
```

Vous devez avoir Python 3.7 ou supérieur. Sinon, téléchargez-le sur [python.org](https://www.python.org/).

### Étape 2 : Organisation des Fichiers
Créez un dossier `swgoh-manager` et placez-y tous les fichiers :
```
swgoh-manager/
├── app.py
├── requirements.txt
├── README.md
├── start.bat (Windows) ou start.sh (Mac/Linux)
└── templates/
    ├── base.html
    ├── index.html
    ├── mods.html
    ├── optimizer.html
    ├── loadouts.html
    └── gac.html
```

### Étape 3 : Installation Automatique

#### Windows
1. Double-cliquez sur `start.bat`
2. Les dépendances s'installent automatiquement
3. L'application démarre

#### Mac/Linux
1. Rendez le script exécutable :
   ```bash
   chmod +x start.sh
   ```
2. Exécutez-le :
   ```bash
   ./start.sh
   ```

#### Installation Manuelle (si les scripts ne fonctionnent pas)
```bash
pip install Flask requests pandas
python app.py
```

### Étape 4 : Accéder à l'Application
Ouvrez votre navigateur et allez à :
```
http://localhost:5000
```

## ⚡ Première Utilisation

### 1. Charger votre Roster
- Sur la page d'accueil, entrez votre **Ally Code** (format : 123-456-789)
- Cliquez sur **"📥 Récupérer les données"**
- Attendez 10-20 secondes
- ✅ Vos données sont chargées !

### 2. Explorer les Fonctionnalités

#### 📦 Mods
- Cliquez sur **"Mods"** dans le menu
- Voyez tous vos mods équipés et non équipés
- Utilisez les filtres pour trouver vos meilleurs mods vitesse

#### ⚙️ Optimizer
- Cliquez sur **"Optimizer"** dans le menu
- Sélectionnez un personnage
- Choisissez "Vitesse Maximum" pour GAC
- Lancez l'optimisation
- Suivez les instructions pour appliquer les changements dans le jeu

#### 💾 Loadouts
- Créez vos configurations d'équipes pour GAC
- Sauvegardez plusieurs setups pour différents événements
- Exportez et partagez avec votre guilde

#### ⚔️ GAC Compare
- Entrez l'Ally Code de votre adversaire
- Obtenez une analyse complète
- Lisez les recommandations stratégiques

## 🎯 Cas d'Usage Rapides

### Préparation GAC (5 minutes)
1. **Dashboard** : Vérifiez que vos données sont à jour
2. **GAC Compare** : Chargez votre adversaire
3. **Optimizer** : Optimisez vos 5 meilleurs personnages
4. **Loadouts** : Créez 3 loadouts de défense

### Optimisation de Mods (10 minutes)
1. **Mods** : Filtrez les mods non équipés avec vitesse +15
2. **Optimizer** : Optimisez vos personnages clés un par un
3. **Application** : Allez dans le jeu et appliquez les changements

### Analyse de Roster (3 minutes)
1. **Dashboard** : Vue d'ensemble de votre progression
2. **Mods** : Export CSV pour analyse dans Excel
3. **Comparaison** : Comparez-vous à un top joueur

## 🔧 Commandes Utiles

### Arrêter le Serveur
Appuyez sur `Ctrl + C` dans le terminal

### Redémarrer l'Application
```bash
python app.py
```

### Mettre à Jour les Dépendances
```bash
pip install --upgrade Flask requests pandas
```

### Réinitialiser la Base de Données
```bash
# Sauvegardez d'abord !
cp swgoh_data.db swgoh_data.db.backup

# Supprimez la base
rm swgoh_data.db  # Mac/Linux
del swgoh_data.db  # Windows

# Redémarrez l'app
python app.py
```

## ❓ Problèmes Courants

### "Module 'flask' not found"
```bash
pip install Flask
```

### "Port 5000 already in use"
Modifiez le port dans `app.py` :
```python
app.run(debug=True, port=5001)  # Changez 5000 en 5001
```

### "Unable to connect to API"
- Vérifiez votre connexion Internet
- L'API SWGOH.gg peut être temporairement down
- Réessayez dans quelques minutes

### Données incorrectes ou anciennes
```bash
# Actualisez vos données depuis le Dashboard
# Cliquez sur "🔄 Actualiser"
```

## 📱 Accès depuis Mobile

Si vous voulez accéder à l'app depuis votre téléphone/tablette :

1. **Trouvez l'IP de votre ordinateur** :
   - Windows : `ipconfig`
   - Mac/Linux : `ifconfig`
   - Cherchez quelque chose comme `192.168.1.XXX`

2. **Sur votre mobile**, ouvrez le navigateur et allez à :
   ```
   http://[IP_DE_VOTRE_PC]:5000
   ```
   Exemple : `http://192.168.1.100:5000`

3. **Note** : Votre ordinateur et mobile doivent être sur le même réseau WiFi

## 💡 Conseils Pro

### Performance
- ⚡ Actualisez vos données 1 fois par jour maximum
- 📊 Utilisez les filtres pour accélérer l'affichage
- 💾 Exportez régulièrement vos loadouts

### Optimisation
- 🎯 Commencez par optimiser vos personnages GAC prioritaires
- ⚖️ Utilisez les presets avant de personnaliser
- 📝 Prenez des notes sur les configurations qui fonctionnent

### Organisation
- 📁 Créez des loadouts distincts pour chaque événement
- 🏷️ Nommez clairement vos configurations
- 💾 Faites des sauvegardes régulières de `swgoh_data.db`

## 🎓 Prochaines Étapes

Maintenant que vous êtes lancé :

1. ✅ Explorez toutes les sections
2. ✅ Créez vos premiers loadouts
3. ✅ Optimisez votre top 10
4. ✅ Préparez votre prochain GAC
5. ✅ Partagez vos configurations avec votre guilde

## 📚 Ressources

- **Documentation complète** : Lisez `README.md`
- **Support** : Consultez la section Dépannage
- **Communauté SWGOH** : Rejoignez le Discord officiel

---

**Prêt à dominer la galaxie ?** ⚔️✨

**May the Force be with you!**