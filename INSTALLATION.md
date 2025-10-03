# 🚀 Installation SWGOH Manager avec Cloudscraper

Guide d'installation complet pour faire fonctionner l'application avec le scraping SWGOH.gg

---

## 📋 Prérequis

- Python 3.7 ou supérieur
- pip3
- Connexion Internet

---

## ⚡ Installation Rapide (Automatique)

### Étape 1 : Installation des dépendances

```bash
pip3 install cloudscraper beautifulsoup4 lxml flask pandas requests
```

### Étape 2 : Test de cloudscraper

```bash
# Créez le fichier test_cloudscraper.py et lancez
python3 test_cloudscraper.py 299146629
```

Vous devriez voir :
```
✅ cloudscraper importé
✅ beautifulsoup4 importé
✅ Connexion réussie !
👤 Joueur trouvé: [Nom du joueur]
🎉 TOUS LES TESTS SONT PASSÉS !
```

### Étape 3 : Patch automatique de app.py

```bash
# Créez le fichier patch_app.py et lancez
python3 patch_app.py
```

### Étape 4 : Lancement de l'application

```bash
python3 app.py
```

Ouvrez votre navigateur : http://localhost:5000

---

## 🔧 Installation Manuelle

Si le patch automatique ne fonctionne pas, suivez ces étapes :

### 1. Sauvegardez votre app.py

```bash
cp app.py app.py.backup
```

### 2. Ajoutez les imports

Ouvrez `app.py` et ajoutez après les autres imports (ligne ~10) :

```python
import cloudscraper
from bs4 import BeautifulSoup
import re
```

### 3. Remplacez la section API HELPERS

Trouvez la ligne `# ==================== API HELPERS ====================`

Remplacez **TOUT** le code entre cette ligne et `# ==================== OPTIMISATION ====================`

Par le code fourni dans l'artefact `swgoh_cloudscraper`.

### 4. Vérifiez les imports dans les fonctions

Assurez-vous que ces fonctions sont présentes :
- `fetch_player_data(ally_code)` ✅
- `parse_character_roster(html)` ✅
- `parse_character_card(card)` ✅
- `generate_demo_data(ally_code)` ✅
- `save_player_data(ally_code, data)` ✅

---

## ✅ Vérification de l'installation

### Test 1 : Imports

```python
python3 -c "import cloudscraper; from bs4 import BeautifulSoup; print('✅ OK')"
```

### Test 2 : Connexion SWGOH.gg

```bash
python3 test_cloudscraper.py 299146629
```

### Test 3 : Lancement de l'application

```bash
python3 app.py
```

Dans le terminal vous devriez voir :
```
Initialisation de la base de données...
Base de données prête!
==================================================
SWGOH Personal Manager - Serveur démarré
==================================================
```

### Test 4 : Test dans le navigateur

1. Ouvrez http://localhost:5000
2. Entrez votre Ally Code (ex: 299146629)
3. Cliquez sur "Charger les données"

Vous devriez voir dans le terminal :
```
============================================================
🔍 Récupération des données pour: 299146629
============================================================
📡 URL: https://swgoh.gg/p/299146629/
✅ Page récupérée avec succès
👤 Joueur: [Votre nom]
🏰 Guilde: [Votre guilde]
⚡ GP Total: [Votre GP]
📋 Récupération du roster...
✅ Page roster récupérée
✅ XXX personnages extraits
============================================================
```

---

## 🐛 Résolution des problèmes

### Erreur: `ModuleNotFoundError: No module named 'cloudscraper'`

**Solution :**
```bash
pip3 install cloudscraper
```

### Erreur: `ModuleNotFoundError: No module named 'bs4'`

**Solution :**
```bash
pip3 install beautifulsoup4
```

### Erreur 403 - Cloudflare bloque toujours

**Vérifications :**
1. Cloudscraper est bien installé ?
   ```bash
   pip3 show cloudscraper
   ```

2. La version est récente ?
   ```bash
   pip3 install --upgrade cloudscraper
   ```

3. Test direct :
   ```python
   import cloudscraper
   scraper = cloudscraper.create_scraper()
   response = scraper.get('https://swgoh.gg/p/299146629/')
   print(response.status_code)  # Devrait afficher 200
   ```

### Aucun personnage trouvé

**Causes possibles :**
1. Le profil SWGOH.gg est vide
2. Le profil est privé
3. L'Ally Code est incorrect

**Test :**
Ouvrez https://swgoh.gg/p/VOTRE_ALLY_CODE/ dans votre navigateur

### L'application ne démarre pas

**Vérifications :**
```bash
# Vérifiez Python
python3 --version

# Vérifiez Flask
pip3 show flask

# Vérifiez le port 5000
lsof -i :5000
# Ou sur Windows
netstat -ano | findstr :5000
```

---

## 📊 Structure des données récupérées

L'application récupère :

### Profil joueur
- ✅ Nom du joueur
- ✅ Nom de la guilde
- ✅ Galactic Power total
- ✅ GP Personnages
- ✅ GP Vaisseaux

### Roster
Pour chaque personnage :
- ✅ Nom
- ✅ Base ID
- ✅ Niveau
- ✅ Gear Level
- ✅ Relic Tier
- ✅ Galactic Power

### Non récupéré (pour l'instant)
- ❌ Mods détaillés (nécessite une page séparée par personnage)
- ❌ Zetas (peut être ajouté)
- ❌ Omicrons (peut être ajouté)
- ❌ Datacrons (peut être ajouté)

---

## 🔄 Mise à jour des données

Pour mettre à jour vos données :

1. Cliquez sur "Charger les données" dans l'interface
2. Entrez à nouveau votre Ally Code
3. Les anciennes données seront remplacées

**Note :** La base de données conserve l'historique via les champs `last_updated`.

---

## 🎯 Optimisations possibles

### Cache local
Ajoutez un cache pour éviter de requêter SWGOH.gg à chaque fois :

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def fetch_player_data_cached(ally_code, cache_time):
    return fetch_player_data(ally_code)

# Utilisation
cache_key = datetime.now().strftime("%Y%m%d%H")  # Cache 1h
data = fetch_player_data_cached(ally_code, cache_key)
```

### Récupération des mods
Pour récupérer les mods détaillés, il faut :
1. Aller sur `https://swgoh.gg/p/{ally_code}/characters/{character_name}/`
2. Parser les mods pour chaque personnage
3. **Attention :** Cela fait beaucoup de requêtes !

---

## 📞 Support

En cas de problème :

1. **Vérifiez les logs** dans le terminal
2. **Testez cloudscraper** : `python3 test_cloudscraper.py`
3. **Vérifiez SWGOH.gg** : Le site est-il accessible ?
4. **Restaurez la sauvegarde** si nécessaire : `cp app.py.backup app.py`

---

## 📝 Changelog

### Version avec Cloudscraper
- ✅ Contournement de la protection Cloudflare
- ✅ Scraping robuste du profil
- ✅ Extraction du roster complet
- ✅ Support JSON et HTML parsing
- ✅ Logs détaillés
- ✅ Gestion d'erreurs améliorée

---

## 🎉 C'est tout !

Vous devriez maintenant avoir une application fonctionnelle qui récupère vos données SWGOH depuis SWGOH.gg.

**Bon farming ! 🚀**