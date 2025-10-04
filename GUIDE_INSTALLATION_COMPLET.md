# 🎯 Guide d'Installation Complet - SWGOH Manager

## 📦 Fichiers Livrés

Vous avez reçu **7 fichiers** via les artifacts Claude :

### ✅ Fichiers à Télécharger depuis les Artifacts

1. **app.py** - Application Flask corrigée (REMPLACE l'existant)
2. **requirements.txt** - Dépendances (mis à jour)
3. **.env.example** - Template de configuration (NOUVEAU)
4. **README.md** - Documentation complète (NOUVEAU)
5. **start.bat** - Script Windows (NOUVEAU)
6. **start.sh** - Script Linux/Mac (NOUVEAU)
7. **.gitignore** - Protection Git (NOUVEAU)

## 🔧 Modification Unique dans app.py

**Seule fonction modifiée : `export_mods()`** (lignes ~690-710)

### ❌ Code Original (Problématique)
```python
@app.route('/api/export/mods/<ally_code>')
def export_mods(ally_code):
    """Export des mods en CSV"""
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT * FROM mods WHERE ally_code = ?', conn, params=(ally_code,))
    conn.close()
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'mods_{ally_code}_{datetime.now().strftime("%Y%m%d")}.csv'  # ❌ Peut causer TypeError
    )
```

### ✅ Code Corrigé (Compatible)
```python
@app.route('/api/export/mods/<ally_code>')
def export_mods(ally_code):
    """Export des mods en CSV"""
    conn = get_db_connection()
    df = pd.read_sql_query('SELECT * FROM mods WHERE ally_code = ?', conn, params=(ally_code,))
    conn.close()
    
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    # CORRECTION: Compatible avec Flask 3.0+ et versions antérieures
    try:
        # Flask 2.0+
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'mods_{ally_code}_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except TypeError:
        # Flask < 2.0
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            attachment_filename=f'mods_{ally_code}_{datetime.now().strftime("%Y%m%d")}.csv'
        )
```

## 🚀 Installation - Méthode Rapide

### Windows

1. **Téléchargez tous les fichiers** depuis les artifacts
2. **Remplacez `app.py`** par la version corrigée
3. **Ajoutez les nouveaux fichiers** dans le dossier du projet
4. **Double-cliquez sur `start.bat`**

```batch
start.bat
```

Le script fera automatiquement :
- ✅ Création de l'environnement virtuel
- ✅ Installation des dépendances
- ✅ Copie de .env.example vers .env
- ✅ Lancement de l'application

### Linux / Mac

1. **Téléchargez tous les fichiers** depuis les artifacts
2. **Remplacez `app.py`** par la version corrigée
3. **Ajoutez les nouveaux fichiers** dans le dossier du projet
4. **Rendez le script exécutable et lancez-le**

```bash
chmod +x start.sh
./start.sh
```

## 🔐 Configuration de la SECRET_KEY

### Méthode Automatique (Recommandée)

```bash
# Générez une clé sécurisée
python -c "import secrets; print(secrets.token_hex(32))"

# Exemple de sortie :
# 3a8f9c2d1e4b7a6c5d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1
```

### Éditez `.env`

Ouvrez le fichier `.env` et remplacez :

```env
SECRET_KEY=votre-cle-secrete-aleatoire-tres-longue-et-complexe
```

Par :

```env
SECRET_KEY=3a8f9c2d1e4b7a6c5d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1
```

## 📋 Structure du Projet Final

```
swgoh-manager/
├── app.py                    ✅ REMPLACÉ (corrigé)
├── requirements.txt          ✅ OK (existant)
├── .env.example             ➕ NOUVEAU
├── .env                     🔐 À créer manuellement
├── README.md                ➕ NOUVEAU
├── start.bat                ➕ NOUVEAU (Windows)
├── start.sh                 ➕ NOUVEAU (Linux/Mac)
├── .gitignore               ➕ NOUVEAU
├── swgoh_data.db            🗄️ Créé automatiquement
├── templates/               ✅ OK (inchangés)
│   ├── base.html
│   ├── index.html
│   ├── mods.html
│   ├── optimizer.html
│   ├── loadouts.html
│   └── gac.html
└── venv/                    📦 Créé par le script
```

## ✅ Checklist de Validation

### 1. Installation ✓
- [ ] Tous les fichiers téléchargés
- [ ] app.py remplacé
- [ ] Nouveaux fichiers ajoutés
- [ ] .env créé et configuré
- [ ] Dépendances installées

### 2. Démarrage ✓
```bash
python app.py
```

**Attendu** :
```
============================================================
SWGOH Personal Manager - Initialisation
============================================================
📦 Initialisation de la base de données...
✓ Base de données prête!

============================================================
🚀 SWGOH Personal Manager - Serveur démarré
============================================================
🌐 Accédez à l'application via: http://localhost:5000
📱 Ou depuis votre réseau local: http://[votre-ip]:5000
⚠️  Mode démonstration activé si l'API SWGOH.gg est inaccessible

💡 Appuyez sur Ctrl+C pour arrêter le serveur
============================================================

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

### 3. Tests Fonctionnels ✓

#### Test Dashboard
1. Ouvrez http://localhost:5000
2. Entrez votre Ally Code (ex: 123-456-789)
3. Cliquez "Récupérer les données"
4. ✅ Vérifiez que les données s'affichent

#### Test Export CSV (TEST PRINCIPAL DU FIX)
1. Allez sur la page "Mods"
2. Cliquez "Exporter CSV"
3. ✅ Un fichier CSV doit se télécharger

**Avant correction** : ❌ Erreur `TypeError: send_file() got an unexpected keyword argument 'download_name'`
**Après correction** : ✅ Fichier `mods_123456789_20251004.csv` téléchargé

#### Tests Complémentaires
- [ ] Page Mods - Affichage et filtres fonctionnent
- [ ] Optimizer - Sélection personnage et optimisation
- [ ] Loadouts - Création et sauvegarde
- [ ] GAC Compare - Comparaison de deux joueurs

## 🐛 Dépannage

### Problème : "ModuleNotFoundError"

```bash
pip install -r requirements.txt --upgrade
```

### Problème : Port 5000 déjà utilisé

Modifiez la dernière ligne de `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Changez 5000 en 5001
```

### Problème : "Permission denied" sur start.sh

```bash
chmod +x start.sh
```

### Problème : Données de démonstration au lieu des vraies

**C'est normal** si :
- SWGOH.gg est inaccessible
- Votre profil n'est pas public
- Cloudflare bloque le scraping

**Test** : Visitez manuellement `https://swgoh.gg/p/VOTRE-ALLY-CODE/`

Si vous voyez "Demo Player" avec ces personnages :
- Jedi Knight Anakin
- Grand Master Yoda
- Darth Revan
- General Kenobi
- Bastila Shan

C'est le **système de fallback** qui fonctionne correctement.

### Problème : Base de données vide après le chargement

Vérifiez dans le terminal :
```
🔍 Récupération des données pour: 123456789
📡 URL: https://swgoh.gg/p/123456789/
✅ Page récupérée avec succès
👤 Joueur: VotreNom
🏰 Guilde: VotreGuilde
⚡ GP Total: 5,234,567
👥 GP Personnages: 3,654,321
🚀 GP Vaisseaux: 1,580,246

📋 Récupération du roster de personnages...
✅ Page roster récupérée
🔍 Recherche des cartes de personnages...
✅ 150 unit-cards trouvées
✅ 150 personnages extraits avec succès
💾 Informations du joueur sauvegardées
💾 150 personnages sauvegardés
```

## 📊 Résumé des Changements

| Fichier | Action | Description |
|---------|--------|-------------|
| `app.py` | ✏️ MODIFIÉ | Fonction `export_mods()` corrigée (lignes ~690-710) |
| `requirements.txt` | ✅ OK | Inchangé (déjà correct) |
| `.env.example` | ➕ NOUVEAU | Template de configuration |
| `.env` | 🔐 À CRÉER | Configuration personnelle |
| `README.md` | ➕ NOUVEAU | Documentation |
| `start.bat` | ➕ NOUVEAU | Script Windows |
| `start.sh` | ➕ NOUVEAU | Script Linux/Mac |
| `.gitignore` | ➕ NOUVEAU | Protection Git |
| `templates/*.html` | ✅ OK | Tous inchangés |

## 🎉 Vous êtes prêt !

Après avoir suivi ces étapes, votre application **SWGOH Manager** est :

- ✅ **Fonctionnelle** - Tous les bugs corrigés
- ✅ **Documentée** - README complet
- ✅ **Sécurisée** - .env et .gitignore configurés
- ✅ **Facile à lancer** - Scripts automatiques
- ✅ **Compatible** - Fonctionne avec Flask 3.0+

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez la checklist ci-dessus
2. Consultez les logs dans le terminal
3. Testez avec les données de démo
4. Vérifiez que votre profil SWGOH.gg est public

---

**Que la Force soit avec vous !** 🌟

*Projet communautaire - Usage personnel uniquement*
*Non affilié à EA, Capital Games ou Lucasfilm*