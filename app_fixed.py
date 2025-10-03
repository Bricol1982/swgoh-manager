"""
CORRECTIFS pour app.py - À intégrer dans votre fichier principal
Remplacez les fonctions correspondantes
"""

import logging

# Configuration des logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def fetch_player_data(ally_code):
    """Récupère les données du joueur via l'API SWGOH.gg - VERSION CORRIGÉE"""
    try:
        clean_code = ally_code.replace('-', '')
        logger.info(f"Tentative de récupération des données pour: {clean_code}")
        
        url = f"{SWGOH_GG_API_URL}/player/{clean_code}/"
        logger.debug(f"URL appelée: {url}")
        
        response = requests.get(url, timeout=10)
        logger.info(f"Réponse API: Status {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✓ Données reçues pour {data.get('data', {}).get('name', 'Unknown')}")
            return data
        else:
            logger.warning(f"API retourne {response.status_code}, utilisation des données de démo")
            logger.debug(f"Réponse: {response.text[:200]}")
            return generate_demo_data(clean_code)
            
    except requests.exceptions.Timeout:
        logger.error("Timeout lors de l'appel API")
        return generate_demo_data(ally_code.replace('-', ''))
    except requests.exceptions.ConnectionError:
        logger.error("Erreur de connexion à l'API")
        return generate_demo_data(ally_code.replace('-', ''))
    except Exception as e:
        logger.error(f"Erreur inattendue: {str(e)}")
        import traceback
        logger.debug(traceback.format_exc())
        return generate_demo_data(ally_code.replace('-', ''))

@app.route('/api/load_player_data', methods=['POST'])
def load_player_data():
    """Charge les données d'un joueur - VERSION CORRIGÉE avec logs détaillés"""
    try:
        # Récupération de l'ally code
        ally_code = request.json.get('ally_code', '').replace('-', '').strip()
        logger.info(f"=== Début chargement données pour {ally_code} ===")
        
        # Validation
        if not ally_code:
            logger.warning("Ally code vide")
            return jsonify({'error': 'Ally Code requis'}), 400
            
        if len(ally_code) != 9 or not ally_code.isdigit():
            logger.warning(f"Ally code invalide: {ally_code} (longueur: {len(ally_code)})")
            return jsonify({'error': 'Ally Code invalide (9 chiffres requis)'}), 400
        
        logger.info(f"Ally code validé: {ally_code}")
        
        # Récupère les données
        logger.info("Appel à fetch_player_data...")
        data = fetch_player_data(ally_code)
        
        if not data:
            logger.error("Aucune donnée retournée par fetch_player_data")
            return jsonify({'error': 'Impossible de récupérer les données'}), 500
        
        logger.info("Données récupérées, début sauvegarde...")
        
        # Sauvegarde dans la DB
        if save_player_data(ally_code, data):
            logger.info("✓ Données sauvegardées avec succès")
            
            # Récupère les stats pour le dashboard
            conn = get_db_connection()
            c = conn.cursor()
            
            try:
                # Info joueur
                c.execute('SELECT * FROM player_info WHERE ally_code = ?', (ally_code,))
                player_row = c.fetchone()
                
                if not player_row:
                    logger.error("Impossible de retrouver le joueur après sauvegarde")
                    return jsonify({'error': 'Erreur après sauvegarde'}), 500
                
                player = dict(player_row)
                logger.debug(f"Joueur: {player['name']}")
                
                # Statistiques
                c.execute('SELECT COUNT(*) as count FROM characters WHERE ally_code = ?', (ally_code,))
                total_chars = c.fetchone()['count']
                
                c.execute('SELECT COUNT(*) as count FROM characters WHERE ally_code = ? AND relic_tier >= 5', 
                          (ally_code,))
                relics_r5 = c.fetchone()['count']
                
                c.execute('SELECT COUNT(*) as count FROM mods WHERE ally_code = ?', (ally_code,))
                total_mods = c.fetchone()['count']
                
                logger.debug(f"Stats: {total_chars} persos, {relics_r5} R5+, {total_mods} mods")
                
                # Top 10 personnages
                c.execute('''SELECT name, galactic_power as gp FROM characters 
                             WHERE ally_code = ? 
                             ORDER BY galactic_power DESC LIMIT 10''', 
                          (ally_code,))
                top_chars = [dict(row) for row in c.fetchall()]
                
                logger.info(f"✓ Chargement terminé: {len(top_chars)} top characters")
                
                response_data = {
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
                }
                
                logger.debug(f"Réponse préparée: {response_data}")
                return jsonify(response_data)
                
            except Exception as e:
                logger.error(f"Erreur lors de la récupération des stats: {str(e)}")
                import traceback
                logger.debug(traceback.format_exc())
                return jsonify({'error': 'Erreur lors de la récupération des statistiques'}), 500
            finally:
                conn.close()
        else:
            logger.error("Échec de la sauvegarde")
            return jsonify({'error': 'Erreur lors de la sauvegarde'}), 500
            
    except Exception as e:
        logger.error(f"Erreur critique dans load_player_data: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

def save_player_data(ally_code, data):
    """Sauvegarde les données - VERSION CORRIGÉE avec logs"""
    conn = get_db_connection()
    c = conn.cursor()
    
    try:
        player_data = data.get('data', data)
        logger.debug(f"Sauvegarde joueur: {player_data.get('name', 'Unknown')}")
        
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
        
        logger.debug("Info joueur sauvegardée")
        
        # Supprime les anciennes données
        c.execute('DELETE FROM characters WHERE ally_code = ?', (ally_code,))
        c.execute('DELETE FROM mods WHERE ally_code = ?', (ally_code,))
        logger.debug("Anciennes données supprimées")
        
        # Sauvegarde personnages
        roster = player_data.get('roster', [])
        logger.info(f"Sauvegarde de {len(roster)} unités")
        
        char_count = 0
        for unit in roster:
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
                
                char_count += 1
                
                # Sauvegarde mods équipés
                for mod in unit.get('mods', []):
                    save_mod(c, ally_code, unit.get('base_id'), mod, is_equipped=True)
        
        logger.info(f"✓ {char_count} personnages sauvegardés")
        
        conn.commit()
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        conn.rollback()
        return False
    finally:
        conn.close()