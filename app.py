"""
SWGOH Personal Manager
Application web personnelle pour la gestion et l'optimisation du roster Star Wars: Galaxy of Heroes
Usage local uniquement - Aucune interaction directe avec le jeu
"""

from flask import Flask, render_template, request, jsonify, send_file
import sqlite3
import requests
import json
import pandas as pd
from datetime import datetime
import io
import base64
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Configuration API - REMPLACEZ PAR VOS CLÉS
SWGOH_HELP_API_URL = "https://api.swgoh.help"
SWGOH_GG_API_URL = "https://swgoh.gg/api"
# Pour SWGOH.help, vous aurez besoin d'un token (inscrivez-vous sur swgoh.help)
API_TOKEN = "YOUR_API_TOKEN_HERE"  # Remplacez par votre token

# ==================== BASE DE DONNÉES ====================

def init_db():
    """Initialise la base de données SQLite"""
    conn = sqlite3.connect('swgoh_data.db')
    c = conn.cursor()
    
    # Table pour les informations du joueur
    c.execute('''CREATE TABLE IF NOT EXISTS player_info (
        ally_code TEXT PRIMARY KEY,
        name TEXT,
        level INTEGER,
        galactic_power INTEGER,
        character_gp INTEGER,
        ship_gp INTEGER,
        last_updated TIMESTAMP
    )''')
    
    # Table pour les personnages
    c.execute('''CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ally_code TEXT,
        base_id TEXT,
        name TEXT,
        level INTEGER,
        gear_level INTEGER,
        relic_tier INTEGER,
        power INTEGER,
        is_zeta INTEGER,
        galactic_power INTEGER,
        FOREIGN KEY (ally_code) REFERENCES player_info(ally_code)
    )''')
    
    # Table pour les mods
    c.execute('''CREATE TABLE IF NOT EXISTS mods (
        id TEXT PRIMARY KEY,
        ally_code TEXT,
        character_id TEXT,
        slot INTEGER,
        set_type TEXT,
        level INTEGER,
        tier INTEGER,
        rarity INTEGER,
        primary_stat_type TEXT,
        primary_stat_value REAL,
        speed REAL DEFAULT 0,
        offense REAL DEFAULT 0,
        offense_percent REAL DEFAULT 0,
        protection REAL DEFAULT 0,
        protection_percent REAL DEFAULT 0,
        health REAL DEFAULT 0,
        health_percent REAL DEFAULT 0,
        defense REAL DEFAULT 0,
        defense_percent REAL DEFAULT 0,
        potency REAL DEFAULT 0,
        tenacity REAL DEFAULT 0,
        critical_chance REAL DEFAULT 0,
        is_equipped INTEGER DEFAULT 1,
        FOREIGN KEY (ally_code) REFERENCES player_info(ally_code)
    )''')
    
    # Table pour les loadouts
    c.execute('''CREATE TABLE IF NOT EXISTS loadouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ally_code TEXT,
        name TEXT,
        description TEXT,
        data TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY (ally_code) REFERENCES player_info(ally_code)
    )''')
    
    # Table pour les priorités d'optimisation
    c.execute('''CREATE TABLE IF NOT EXISTS optimization_priorities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ally_code TEXT,
        character_id TEXT,
        priority_level INTEGER,
        stat_weights TEXT,
        FOREIGN KEY (ally_code) REFERENCES player_info(ally_code)
    )''')
    
    conn.commit()
    conn.close()

# ==================== API HELPERS ====================

def fetch_player_data(ally_code):
    """Récupère les données du joueur via l'API SWGOH.gg (publique et gratuite)"""
    try:
        # Nettoie l'ally code (retire les tirets)
        clean_code = ally_code.replace('-', '')
        
        # SWGOH.gg API (publique, pas besoin de token)
        url = f"{SWGOH_GG_API_URL}/player/{clean_code}/"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Fallback: données de démo si API non disponible
            return generate_demo_data(clean_code)
    except Exception as e:
        print(f"Erreur API: {e}")
        return generate_demo_data(ally_code.replace('-', ''))

def generate_demo_data(ally_code):
    """Génère des données de démonstration pour tests"""
    return {
        'data': {
            'name': 'Demo Player',
            'level': 85,
            'ally_code': ally_code,
            'galactic_power': 5000000,
            'character_galactic_power': 3500000,
            'ship_galactic_power': 1500000,
            'roster': [
                {
                    'base_id': 'ANAKINKNIGHT',
                    'name': 'Jedi Knight Anakin',
                    'level': 85,
                    'gear_level': 13,
                    'relic_tier': 7,
                    'power': 28500,
                    'combat_type': 1,
                    'has_ultimate': False,
                    'mods': []
                },
                {
                    'base_id': 'GRANDMASTERYODA',
                    'name': 'Grand Master Yoda',
                    'level': 85,
                    'gear_level': 12,
                    'relic_tier': 5,
                    'power': 25000,
                    'combat_type': 1,
                    'has_ultimate': False,
                    'mods': []
                }
            ]
        }
    }

def save_player_data(ally_code, data):
    """Sauvegarde les données du joueur dans la base de données"""
    conn = sqlite3.connect('swgoh_data.db')
    c = conn.cursor()
    
    try:
        player_data = data.get('data', data)
        
        # Sauvegarde infos joueur
        c.execute('''INSERT OR REPLACE INTO player_info 
                     (ally_code, name, level, galactic_power, character_gp, ship_gp, last_updated)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (ally_code, 
                   player_data.get('name', 'Unknown'),
                   player_data.get('level', 85),
                   player_data.get('galactic_power', 0),
                   player_data.get('character_galactic_power', 0),
                   player_data.get('ship_galactic_power', 0),
                   datetime.now()))
        
        # Supprime les anciennes données de personnages et mods
        c.execute('DELETE FROM characters WHERE ally_code = ?', (ally_code,))
        c.execute('DELETE FROM mods WHERE ally_code = ?', (ally_code,))
        
        # Sauvegarde personnages
        for unit in player_data.get('roster', []):
            if unit.get('combat_type') == 1:  # Personnages uniquement
                c.execute('''INSERT INTO characters 
                           (ally_code, base_id, name, level, gear_level, relic_tier, power, galactic_power)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                         (ally_code,
                          unit.get('base_id'),
                          unit.get('name'),
                          unit.get('level', 1),
                          unit.get('gear_level', 1),
                          unit.get('relic_tier', 0),
                          unit.get('power', 0),
                          unit.get('galactic_power', 0)))
                
                # Sauvegarde mods équipés
                for mod in unit.get('mods', []):
                    save_mod(c, ally_code, unit.get('base_id'), mod, is_equipped=True)
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur sauvegarde: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def save_mod(cursor, ally_code, character_id, mod_data, is_equipped=True):
    """Sauvegarde un mod dans la base de données"""
    # Extraction des stats secondaires
    secondary_stats = {}
    for stat in mod_data.get('secondary_stats', []):
        stat_type = stat.get('name', '').lower()
        stat_value = stat.get('value', 0)
        
        if 'speed' in stat_type:
            secondary_stats['speed'] = stat_value
        elif 'offense' in stat_type and '%' not in stat_type:
            secondary_stats['offense'] = stat_value
        elif 'offense' in stat_type and '%' in stat_type:
            secondary_stats['offense_percent'] = stat_value
        # etc. pour autres stats
    
    cursor.execute('''INSERT OR REPLACE INTO mods 
                   (id, ally_code, character_id, slot, set_type, level, tier, rarity,
                    primary_stat_type, primary_stat_value, speed, offense, is_equipped)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (mod_data.get('id', f"{ally_code}_{character_id}_{mod_data.get('slot')}"),
                  ally_code,
                  character_id if is_equipped else None,
                  mod_data.get('slot', 1),
                  mod_data.get('set', 1),
                  mod_data.get('level', 1),
                  mod_data.get('tier', 1),
                  mod_data.get('rarity', 5),
                  mod_data.get('primary_stat', {}).get('name', 'Unknown'),
                  mod_data.get('primary_stat', {}).get('value', 0),
                  secondary_stats.get('speed', 0),
                  secondary_stats.get('offense', 0),
                  1 if is_equipped else 0))

# ==================== OPTIMISATION ====================

def calculate_character_score(character, mod_config, stat_weights):
    """Calcule un score pour un personnage avec une configuration de mods donnée"""
    score = 0
    
    # Stats de base du personnage
    base_stats = {
        'speed': 100 + (character['gear_level'] * 5) + (character['relic_tier'] * 10),
        'offense': 1000 + (character['gear_level'] * 100),
        'protection': 10000 + (character['gear_level'] * 1000)
    }
    
    # Ajoute les stats des mods
    for mod in mod_config:
        base_stats['speed'] += mod.get('speed', 0)
        base_stats['offense'] += mod.get('offense', 0)
        base_stats['protection'] += mod.get('protection', 0)
    
    # Calcule le score pondéré
    for stat, weight in stat_weights.items():
        score += base_stats.get(stat, 0) * weight
    
    return score, base_stats

def optimize_mods_for_character(ally_code, character_id, stat_weights):
    """Optimise les mods pour un personnage spécifique"""
    conn = sqlite3.connect('swgoh_data.db')
    c = conn.cursor()
    
    # Récupère le personnage
    c.execute('SELECT * FROM characters WHERE ally_code = ? AND base_id = ?', 
              (ally_code, character_id))
    character = dict(zip([d[0] for d in c.description], c.fetchone()))
    
    # Récupère tous les mods non équipés + ceux du personnage
    c.execute('''SELECT * FROM mods 
                 WHERE ally_code = ? AND (is_equipped = 0 OR character_id = ?)''',
              (ally_code, character_id))
    
    available_mods = [dict(zip([d[0] for d in c.description], row)) for row in c.fetchall()]
    conn.close()
    
    # Groupe les mods par slot
    mods_by_slot = defaultdict(list)
    for mod in available_mods:
        mods_by_slot[mod['slot']].append(mod)
    
    # Sélectionne le meilleur mod pour chaque slot
    best_config = []
    for slot in range(1, 7):  # 6 slots de mods
        if slot in mods_by_slot and mods_by_slot[slot]:
            # Trie par vitesse (ou autre stat prioritaire)
            sorted_mods = sorted(mods_by_slot[slot], 
                               key=lambda m: m.get('speed', 0), 
                               reverse=True)
            best_config.append(sorted_mods[0])
    
    # Calcule les stats finales
    score, final_stats = calculate_character_score(character, best_config, stat_weights)
    
    return {
        'character': character,
        'recommended_mods': best_config,
        'final_stats': final_stats,
        'score': score
    }

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Page d'accueil - Dashboard"""
    return render_template('index.html')

@app.route('/mods')
def mods_page():
    """Page de gestion des mods"""
    return render_template('mods.html')

@app.route('/optimizer')
def optimizer_page():
    """Page d'optimisation"""
    return render_template('optimizer.html')

@app.route('/loadouts')
def loadouts_page():
    """Page de gestion des loadouts"""
    return render_template('loadouts.html')

@app.route('/gac')
def gac_page():
    """Page de comparaison GAC"""
    return render_template('gac.html')

@app.route('/api/fetch_player', methods=['POST'])
def fetch_player():
    """Récupère et sauvegarde les données d'un joueur"""
    ally_code = request.json.get('ally_code', '').replace('-', '')
    
    if not ally_code:
        return jsonify({'error': 'AllyCode requis'}), 400
    
    # Fetch data
    data = fetch_player_data(ally_code)
    
    if data:
        # Sauvegarde dans la DB
        if save_player_data(ally_code, data):
            return jsonify({
                'success': True,
                'message': 'Données récupérées avec succès',
                'data': {
                    'name': data.get('data', {}).get('name'),
                    'gp': data.get('data', {}).get('galactic_power'),
                    'characters': len([u for u in data.get('data', {}).get('roster', []) 
                                     if u.get('combat_type') == 1])
                }
            })
        else:
            return jsonify({'error': 'Erreur lors de la sauvegarde'}), 500
    else:
        return jsonify({'error': 'Impossible de récupérer les données'}), 500

@app.route('/api/player_info/<ally_code>')
def get_player_info(ally_code):
    """Récupère les infos d'un joueur depuis la DB"""
    conn = sqlite3.connect('swgoh_data.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM player_info WHERE ally_code = ?', (ally_code,))
    row = c.fetchone()
    
    if row:
        player = dict(zip([d[0] for d in c.description], row))
        
        # Récupère le nombre de personnages
        c.execute('SELECT COUNT(*) FROM characters WHERE ally_code = ?', (ally_code,))
        char_count = c.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'player': player,
            'character_count': char_count
        })
    else:
        conn.close()
        return jsonify({'error': 'Joueur non trouvé'}), 404

@app.route('/api/characters/<ally_code>')
def get_characters(ally_code):
    """Récupère tous les personnages d'un joueur"""
    conn = sqlite3.connect('swgoh_data.db')
    df = pd.read_sql_query(
        'SELECT * FROM characters WHERE ally_code = ? ORDER BY galactic_power DESC',
        conn, params=(ally_code,)
    )
    conn.close()
    
    return jsonify({
        'success': True,
        'characters': df.to_dict('records')
    })

@app.route('/api/mods/<ally_code>')
def get_mods(ally_code):
    """Récupère tous les mods d'un joueur"""
    conn = sqlite3.connect('swgoh_data.db')
    
    equipped = request.args.get('equipped', 'all')
    
    if equipped == 'yes':
        query = 'SELECT * FROM mods WHERE ally_code = ? AND is_equipped = 1'
    elif equipped == 'no':
        query = 'SELECT * FROM mods WHERE ally_code = ? AND is_equipped = 0'
    else:
        query = 'SELECT * FROM mods WHERE ally_code = ?'
    
    df = pd.read_sql_query(query, conn, params=(ally_code,))
    conn.close()
    
    return jsonify({
        'success': True,
        'mods': df.to_dict('records'),
        'total': len(df),
        'unequipped': len(df[df['is_equipped'] == 0]) if 'is_equipped' in df.columns else 0
    })

@app.route('/api/optimize', methods=['POST'])
def optimize():
    """Optimise les mods pour un personnage"""
    data = request.json
    ally_code = data.get('ally_code')
    character_id = data.get('character_id')
    
    # Poids par défaut (personnalisables)
    stat_weights = data.get('stat_weights', {
        'speed': 1.0,
        'offense': 0.5,
        'protection': 0.3
    })
    
    result = optimize_mods_for_character(ally_code, character_id, stat_weights)
    
    return jsonify({
        'success': True,
        'optimization': result
    })

@app.route('/api/loadout/save', methods=['POST'])
def save_loadout():
    """Sauvegarde un loadout"""
    data = request.json
    ally_code = data.get('ally_code')
    name = data.get('name')
    description = data.get('description', '')
    loadout_data = json.dumps(data.get('data', {}))
    
    conn = sqlite3.connect('swgoh_data.db')
    c = conn.cursor()
    
    c.execute('''INSERT INTO loadouts (ally_code, name, description, data, created_at)
                 VALUES (?, ?, ?, ?, ?)''',
              (ally_code, name, description, loadout_data, datetime.now()))
    
    conn.commit()
    loadout_id = c.lastrowid
    conn.close()
    
    return jsonify({
        'success': True,
        'loadout_id': loadout_id,
        'message': 'Loadout sauvegardé'
    })

@app.route('/api/loadouts/<ally_code>')
def get_loadouts(ally_code):
    """Récupère tous les loadouts d'un joueur"""
    conn = sqlite3.connect('swgoh_data.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM loadouts WHERE ally_code = ? ORDER BY created_at DESC',
              (ally_code,))
    
    loadouts = []
    for row in c.fetchall():
        loadout = dict(zip([d[0] for d in c.description], row))
        loadout['data'] = json.loads(loadout['data'])
        loadouts.append(loadout)
    
    conn.close()
    
    return jsonify({
        'success': True,
        'loadouts': loadouts
    })

@app.route('/api/export/mods/<ally_code>')
def export_mods(ally_code):
    """Export des mods en CSV"""
    conn = sqlite3.connect('swgoh_data.db')
    df = pd.read_sql_query('SELECT * FROM mods WHERE ally_code = ?', conn, params=(ally_code,))
    conn.close()
    
    # Crée un CSV en mémoire
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'mods_{ally_code}_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/api/compare', methods=['POST'])
def compare_players():
    """Compare deux joueurs pour GAC"""
    data = request.json
    ally_code_1 = data.get('ally_code_1')
    ally_code_2 = data.get('ally_code_2')
    
    conn = sqlite3.connect('swgoh_data.db')
    
    # Récupère les infos des deux joueurs
    c = conn.cursor()
    c.execute('SELECT * FROM player_info WHERE ally_code IN (?, ?)', 
              (ally_code_1, ally_code_2))
    players = [dict(zip([d[0] for d in c.description], row)) for row in c.fetchall()]
    
    # Compare les rosters
    df1 = pd.read_sql_query('SELECT * FROM characters WHERE ally_code = ?',
                            conn, params=(ally_code_1,))
    df2 = pd.read_sql_query('SELECT * FROM characters WHERE ally_code = ?',
                            conn, params=(ally_code_2,))
    
    conn.close()
    
    comparison = {
        'players': players,
        'stats': {
            'player1': {
                'total_characters': len(df1),
                'avg_gear': df1['gear_level'].mean(),
                'avg_relic': df1['relic_tier'].mean(),
                'top_gp': df1.nlargest(10, 'galactic_power')['galactic_power'].sum()
            },
            'player2': {
                'total_characters': len(df2),
                'avg_gear': df2['gear_level'].mean(),
                'avg_relic': df2['relic_tier'].mean(),
                'top_gp': df2.nlargest(10, 'galactic_power')['galactic_power'].sum()
            }
        }
    }
    
    return jsonify({
        'success': True,
        'comparison': comparison
    })

if __name__ == '__main__':
    print("Initialisation de la base de données...")
    init_db()
    print("Base de données prête!")
    print("\n" + "="*50)
    print("SWGOH Personal Manager - Serveur démarré")
    print("="*50)
    print("Accédez à l'application via: http://localhost:5000")
    print("Appuyez sur Ctrl+C pour arrêter le serveur")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)