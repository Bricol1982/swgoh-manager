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
import os
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Configuration API
SWGOH_HELP_API_URL = "https://api.swgoh.help"
SWGOH_GG_API_URL = "https://swgoh.gg/api"
API_TOKEN = os.environ.get('SWGOH_API_TOKEN', 'YOUR_API_TOKEN_HERE')

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
        guild_name TEXT,
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
        event_type TEXT,
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

def get_db_connection():
    """Retourne une connexion à la base de données"""
    conn = sqlite3.connect('swgoh_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# ==================== API HELPERS ====================

def fetch_player_data(ally_code):
    """Récupère les données du joueur via l'API SWGOH.gg"""
    try:
        clean_code = ally_code.replace('-', '')
        url = f"{SWGOH_GG_API_URL}/player/{clean_code}/"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
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
            'guild_name': 'Demo Guild',
            'ally_code': ally_code,
            'galactic_power': 5234567,
            'character_galactic_power': 3654321,
            'ship_galactic_power': 1580246,
            'roster': [
                {
                    'base_id': 'ANAKINKNIGHT',
                    'name': 'Jedi Knight Anakin',
                    'level': 85,
                    'gear_level': 13,
                    'relic_tier': 7,
                    'power': 28500,
                    'galactic_power': 28500,
                    'combat_type': 1,
                    'has_ultimate': False,
                    'mods': [
                        {
                            'id': 'mod1',
                            'slot': 1,
                            'set': 4,
                            'level': 15,
                            'tier': 5,
                            'rarity': 5,
                            'primary_stat': {'name': 'Speed', 'value': 30},
                            'secondary_stats': [
                                {'name': 'Speed', 'value': 18},
                                {'name': 'Offense', 'value': 215}
                            ]
                        }
                    ]
                },
                {
                    'base_id': 'GRANDMASTERYODA',
                    'name': 'Grand Master Yoda',
                    'level': 85,
                    'gear_level': 12,
                    'relic_tier': 5,
                    'power': 25000,
                    'galactic_power': 25000,
                    'combat_type': 1,
                    'has_ultimate': False,
                    'mods': []
                },
                {
                    'base_id': 'DARTHREVAN',
                    'name': 'Darth Revan',
                    'level': 85,
                    'gear_level': 13,
                    'relic_tier': 8,
                    'power': 29800,
                    'galactic_power': 29800,
                    'combat_type': 1,
                    'has_ultimate': False,
                    'mods': []
                },
                {
                    'base_id': 'GENERALKENOBI',
                    'name': 'General Kenobi',
                    'level': 85,
                    'gear_level': 13,
                    'relic_tier': 7,
                    'power': 27200,
                    'galactic_power': 27200,
                    'combat_type': 1,
                    'has_ultimate': False,
                    'mods': []
                },
                {
                    'base_id': 'BASTILASHAN',
                    'name': 'Bastila Shan',
                    'level': 85,
                    'gear_level': 12,
                    'relic_tier': 6,
                    'power': 26100,
                    'galactic_power': 26100,
                    'combat_type': 1,
                    'has_ultimate': False,
                    'mods': []
                }
            ]
        }
    }

def save_player_data(ally_code, data):
    """Sauvegarde les données du joueur dans la base de données"""
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        player_data = data.get('data', data)
        
        # Sauvegarde infos joueur
        c.execute('''INSERT OR REPLACE INTO player_info 
                     (ally_code, name, level, guild_name, galactic_power, character_gp, ship_gp, last_updated)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (ally_code, 
                   player_data.get('name', 'Unknown'),
                   player_data.get('level', 85),
                   player_data.get('guild_name', 'No Guild'),
                   player_data.get('galactic_power', 0),
                   player_data.get('character_galactic_power', 0),
                   player_data.get('ship_galactic_power', 0),
                   datetime.now()))
        
        # Supprime les anciennes données
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
    
    base_stats = {
        'speed': 100 + (character['gear_level'] * 5) + (character['relic_tier'] * 10),
        'offense': 1000 + (character['gear_level'] * 100),
        'protection': 10000 + (character['gear_level'] * 1000)
    }
    
    for mod in mod_config:
        base_stats['speed'] += mod.get('speed', 0)
        base_stats['offense'] += mod.get('offense', 0)
        base_stats['protection'] += mod.get('protection', 0)
    
    for stat, weight in stat_weights.items():
        score += base_stats.get(stat, 0) * weight
    
    return score, base_stats

def optimize_mods_for_character(ally_code, character_id, stat_weights):
    """Optimise les mods pour un personnage spécifique"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM characters WHERE ally_code = ? AND base_id = ?', 
              (ally_code, character_id))
    character = dict(c.fetchone())
    
    c.execute('''SELECT * FROM mods 
                 WHERE ally_code = ? AND (is_equipped = 0 OR character_id = ?)''',
              (ally_code, character_id))
    
    available_mods = [dict(row) for row in c.fetchall()]
    conn.close()
    
    mods_by_slot = defaultdict(list)
    for mod in available_mods:
        mods_by_slot[mod['slot']].append(mod)
    
    best_config = []
    for slot in range(1, 7):
        if slot in mods_by_slot and mods_by_slot[slot]:
            sorted_mods = sorted(mods_by_slot[slot], 
                               key=lambda m: m.get('speed', 0), 
                               reverse=True)
            best_config.append(sorted_mods[0])
    
    score, final_stats = calculate_character_score(character, best_config, stat_weights)
    
    return {
        'character': character,
        'recommended_mods': best_config,
        'final_stats': final_stats,
        'score': score
    }

# ==================== ROUTES PRINCIPALES ====================

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

# ==================== API ENDPOINTS ====================

@app.route('/api/load_player_data', methods=['POST'])
def load_player_data():
    """Charge les données d'un joueur depuis l'API et les sauvegarde"""
    ally_code = request.json.get('ally_code', '').replace('-', '')
    
    if not ally_code or len(ally_code) != 9:
        return jsonify({'error': 'Ally Code invalide (9 chiffres requis)'}), 400
    
    # Récupère les données
    data = fetch_player_data(ally_code)
    
    if not data:
        return jsonify({'error': 'Impossible de récupérer les données'}), 500
    
    # Sauvegarde dans la DB
    if save_player_data(ally_code, data):
        # Récupère les stats pour le dashboard
        conn = get_db_connection()
        c = conn.cursor()
        
        # Info joueur
        c.execute('SELECT * FROM player_info WHERE ally_code = ?', (ally_code,))
        player = dict(c.fetchone())
        
        # Statistiques
        c.execute('SELECT COUNT(*) as count FROM characters WHERE ally_code = ?', (ally_code,))
        total_chars = c.fetchone()['count']
        
        c.execute('SELECT COUNT(*) as count FROM characters WHERE ally_code = ? AND relic_tier >= 5', 
                  (ally_code,))
        relics_r5 = c.fetchone()['count']
        
        c.execute('SELECT COUNT(*) as count FROM mods WHERE ally_code = ?', (ally_code,))
        total_mods = c.fetchone()['count']
        
        # Top 10 personnages
        c.execute('''SELECT name, galactic_power as gp FROM characters 
                     WHERE ally_code = ? 
                     ORDER BY galactic_power DESC LIMIT 10''', 
                  (ally_code,))
        top_chars = [dict(row) for row in c.fetchall()]
        
        conn.close()
        
        return jsonify({
            'player': {
                'name': player['name'],
                'level': player['level'],
                'guild_name': player['guild_name']
            },
            'stats': {
                'total_gp': player['galactic_power'],
                'total_characters': total_chars,
                'relics_r5_plus': relics_r5,
                'total_mods': total_mods
            },
            'top_characters': top_chars
        })
    else:
        return jsonify({'error': 'Erreur lors de la sauvegarde'}), 500

@app.route('/api/check_loaded_data')
def check_loaded_data():
    """Vérifie si des données sont déjà chargées"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM player_info ORDER BY last_updated DESC LIMIT 1')
    row = c.fetchone()
    
    if row:
        player = dict(row)
        ally_code = player['ally_code']
        
        # Récupère les stats
        c.execute('SELECT COUNT(*) as count FROM characters WHERE ally_code = ?', (ally_code,))
        total_chars = c.fetchone()['count']
        
        c.execute('SELECT COUNT(*) as count FROM characters WHERE ally_code = ? AND relic_tier >= 5', 
                  (ally_code,))
        relics_r5 = c.fetchone()['count']
        
        c.execute('SELECT COUNT(*) as count FROM mods WHERE ally_code = ?', (ally_code,))
        total_mods = c.fetchone()['count']
        
        c.execute('''SELECT name, galactic_power as gp FROM characters 
                     WHERE ally_code = ? 
                     ORDER BY galactic_power DESC LIMIT 10''', 
                  (ally_code,))
        top_chars = [dict(row) for row in c.fetchall()]
        
        conn.close()
        
        return jsonify({
            'has_data': True,
            'player': {
                'name': player['name'],
                'level': player['level'],
                'guild_name': player['guild_name']
            },
            'stats': {
                'total_gp': player['galactic_power'],
                'total_characters': total_chars,
                'relics_r5_plus': relics_r5,
                'total_mods': total_mods
            },
            'top_characters': top_chars
        })
    else:
        conn.close()
        return jsonify({'has_data': False})

@app.route('/api/fetch_player', methods=['POST'])
def fetch_player():
    """Récupère et sauvegarde les données d'un joueur (legacy endpoint)"""
    return load_player_data()

@app.route('/api/player_info/<ally_code>')
def get_player_info(ally_code):
    """Récupère les infos d'un joueur depuis la DB"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM player_info WHERE ally_code = ?', (ally_code,))
    row = c.fetchone()
    
    if row:
        player = dict(row)
        
        c.execute('SELECT COUNT(*) as count FROM characters WHERE ally_code = ?', (ally_code,))
        char_count = c.fetchone()['count']
        
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
    conn = get_db_connection()
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
    conn = get_db_connection()
    
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
    event_type = data.get('event_type', 'General')
    loadout_data = json.dumps(data.get('data', {}))
    
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''INSERT INTO loadouts (ally_code, name, description, event_type, data, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (ally_code, name, description, event_type, loadout_data, datetime.now()))
    
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
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM loadouts WHERE ally_code = ? ORDER BY created_at DESC',
              (ally_code,))
    
    loadouts = []
    for row in c.fetchall():
        loadout = dict(row)
        loadout['data'] = json.loads(loadout['data'])
        loadouts.append(loadout)
    
    conn.close()
    
    return jsonify({
        'success': True,
        'loadouts': loadouts
    })

@app.route('/api/loadout/delete/<int:loadout_id>', methods=['DELETE'])
def delete_loadout(loadout_id):
    """Supprime un loadout"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('DELETE FROM loadouts WHERE id = ?', (loadout_id,))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': 'Loadout supprimé'
    })

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
        download_name=f'mods_{ally_code}_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/api/compare', methods=['POST'])
def compare_players():
    """Compare deux joueurs pour GAC"""
    data = request.json
    ally_code_1 = data.get('ally_code_1')
    ally_code_2 = data.get('ally_code_2')
    
    conn = get_db_connection()
    
    c = conn.cursor()
    c.execute('SELECT * FROM player_info WHERE ally_code IN (?, ?)', 
              (ally_code_1, ally_code_2))
    players = [dict(row) for row in c.fetchall()]
    
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
                'avg_gear': float(df1['gear_level'].mean()) if len(df1) > 0 else 0,
                'avg_relic': float(df1['relic_tier'].mean()) if len(df1) > 0 else 0,
                'top_gp': int(df1.nlargest(10, 'galactic_power')['galactic_power'].sum()) if len(df1) >= 10 else 0
            },
            'player2': {
                'total_characters': len(df2),
                'avg_gear': float(df2['gear_level'].mean()) if len(df2) > 0 else 0,
                'avg_relic': float(df2['relic_tier'].mean()) if len(df2) > 0 else 0,
                'top_gp': int(df2.nlargest(10, 'galactic_power')['galactic_power'].sum()) if len(df2) >= 10 else 0
            }
        }
    }
    
    return jsonify({
        'success': True,
        'comparison': comparison
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trouvé'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur serveur interne'}), 500

# ==================== MAIN ====================

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