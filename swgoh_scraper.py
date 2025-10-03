"""
Scraper pour récupérer les données depuis les pages SWGOH.gg
Utilise BeautifulSoup pour parser le HTML
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class SWGOHScraper:
    def __init__(self):
        self.base_url = "https://swgoh.gg"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def fetch_player_profile(self, ally_code):
        """Récupère le profil complet d'un joueur"""
        clean_code = ally_code.replace('-', '')
        url = f"{self.base_url}/p/{clean_code}/"
        
        print(f"📡 Récupération du profil: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                print("✓ Page récupérée avec succès")
                return self.parse_profile_page(response.text, clean_code)
            else:
                print(f"✗ Erreur HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ Erreur: {str(e)}")
            return None
    
    def parse_profile_page(self, html, ally_code):
        """Parse la page de profil et extrait les données"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraction du nom du joueur
        player_name = "Unknown"
        name_elem = soup.find('h5', class_='pull-left')
        if name_elem:
            player_name = name_elem.text.strip()
        
        # Extraction de la guilde
        guild_name = "No Guild"
        guild_elem = soup.find('a', href=re.compile(r'/g/'))
        if guild_elem:
            guild_name = guild_elem.text.strip()
        
        # Extraction du Galactic Power
        gp_total = 0
        gp_char = 0
        gp_ship = 0
        
        gp_elements = soup.find_all('div', class_='profile-stat')
        for elem in gp_elements:
            label = elem.find('div', class_='stat-label')
            value = elem.find('div', class_='stat-value')
            
            if label and value:
                label_text = label.text.strip().lower()
                value_text = value.text.strip().replace(',', '').replace(' ', '')
                
                try:
                    if 'galactic power' in label_text and 'character' not in label_text and 'ship' not in label_text:
                        gp_total = int(value_text)
                    elif 'character' in label_text:
                        gp_char = int(value_text)
                    elif 'ship' in label_text:
                        gp_ship = int(value_text)
                except:
                    pass
        
        print(f"✓ Joueur: {player_name}")
        print(f"✓ Guilde: {guild_name}")
        print(f"✓ GP Total: {gp_total:,}")
        
        # Récupération du roster
        roster = self.fetch_character_roster(ally_code)
        
        return {
            'data': {
                'name': player_name,
                'level': 85,
                'guild_name': guild_name,
                'ally_code': ally_code,
                'galactic_power': gp_total,
                'character_galactic_power': gp_char,
                'ship_galactic_power': gp_ship,
                'roster': roster
            }
        }
    
    def fetch_character_roster(self, ally_code):
        """Récupère la liste des personnages"""
        url = f"{self.base_url}/p/{ally_code}/characters/"
        
        print(f"\n📋 Récupération du roster...")
        
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                return self.parse_character_roster(response.text)
            else:
                print(f"✗ Erreur lors de la récupération du roster")
                return []
                
        except Exception as e:
            print(f"✗ Erreur roster: {str(e)}")
            return []
    
    def parse_character_roster(self, html):
        """Parse la page du roster de personnages"""
        soup = BeautifulSoup(html, 'html.parser')
        roster = []
        
        # Cherche les données JSON embarquées dans la page
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'unitsList' in script.string:
                # Extraction du JSON des personnages
                try:
                    # Recherche du pattern JSON
                    match = re.search(r'unitsList\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                    if match:
                        units_data = json.loads(match.group(1))
                        
                        for unit in units_data:
                            character = self.parse_character_data(unit)
                            if character:
                                roster.append(character)
                        
                        print(f"✓ {len(roster)} personnages trouvés")
                        return roster
                except Exception as e:
                    print(f"⚠ Erreur parsing JSON: {str(e)}")
        
        # Fallback: parse les cartes de personnages HTML
        print("ℹ Utilisation du parsing HTML...")
        character_cards = soup.find_all('div', class_='collection-char')
        
        for card in character_cards[:50]:  # Limite pour les tests
            try:
                character = self.parse_character_card(card)
                if character:
                    roster.append(character)
            except Exception as e:
                continue
        
        print(f"✓ {len(roster)} personnages extraits")
        return roster
    
    def parse_character_data(self, unit_data):
        """Parse les données d'un personnage depuis le JSON"""
        try:
            # Extraction des données principales
            base_id = unit_data.get('base_id', '')
            name = unit_data.get('name', 'Unknown')
            
            # Données de combat
            combat_type = unit_data.get('combat_type', 1)
            if combat_type != 1:  # On ne veut que les personnages, pas les vaisseaux
                return None
            
            level = unit_data.get('level', 1)
            gear_level = unit_data.get('gear_level', 1)
            relic_tier = unit_data.get('relic_tier', 0)
            power = unit_data.get('power', 0)
            
            return {
                'base_id': base_id,
                'name': name,
                'level': level,
                'gear_level': gear_level,
                'relic_tier': max(0, relic_tier - 2) if relic_tier > 2 else 0,  # Ajustement format
                'power': power,
                'galactic_power': power,
                'combat_type': 1,
                'has_ultimate': False,
                'mods': []  # Les mods nécessiteraient une requête séparée
            }
        except Exception as e:
            return None
    
    def parse_character_card(self, card):
        """Parse une carte de personnage HTML"""
        try:
            # Nom du personnage
            name_elem = card.find('div', class_='char-name')
            name = name_elem.text.strip() if name_elem else "Unknown"
            
            # Base ID depuis le lien
            link = card.find('a')
            base_id = ""
            if link and 'href' in link.attrs:
                match = re.search(r'/characters/([^/]+)/', link['href'])
                if match:
                    base_id = match.group(1).upper().replace('-', '')
            
            # Gear level
            gear_elem = card.find('div', class_='char-gearing')
            gear_level = 1
            if gear_elem:
                gear_match = re.search(r'(\d+)', gear_elem.text)
                if gear_match:
                    gear_level = int(gear_match.group(1))
            
            # Relic tier
            relic_tier = 0
            relic_elem = card.find('div', class_='char-relic')
            if relic_elem:
                relic_match = re.search(r'(\d+)', relic_elem.text)
                if relic_match:
                    relic_tier = int(relic_match.group(1))
            
            # Power
            power_elem = card.find('div', class_='char-power')
            power = 0
            if power_elem:
                power_text = power_elem.text.replace(',', '').strip()
                power_match = re.search(r'(\d+)', power_text)
                if power_match:
                    power = int(power_match.group(1))
            
            return {
                'base_id': base_id or name.upper().replace(' ', ''),
                'name': name,
                'level': 85,
                'gear_level': gear_level,
                'relic_tier': relic_tier,
                'power': power,
                'galactic_power': power,
                'combat_type': 1,
                'has_ultimate': False,
                'mods': []
            }
        except Exception as e:
            return None

def test_scraper(ally_code):
    """Test du scraper"""
    print("\n" + "="*60)
    print("TEST DU SCRAPER SWGOH.gg")
    print("="*60 + "\n")
    
    scraper = SWGOHScraper()
    data = scraper.fetch_player_profile(ally_code)
    
    if data:
        print("\n" + "="*60)
        print("RÉSULTAT")
        print("="*60)
        player = data['data']
        print(f"Nom: {player['name']}")
        print(f"Guilde: {player['guild_name']}")
        print(f"GP Total: {player['galactic_power']:,}")
        print(f"Personnages: {len(player['roster'])}")
        
        if player['roster']:
            print(f"\nTop 5 personnages:")
            sorted_roster = sorted(player['roster'], key=lambda x: x['galactic_power'], reverse=True)
            for i, char in enumerate(sorted_roster[:5], 1):
                print(f"  {i}. {char['name']} - G{char['gear_level']} R{char['relic_tier']} - {char['galactic_power']:,} GP")
        
        return data
    else:
        print("\n✗ Échec du scraping")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        ally_code = sys.argv[1]
    else:
        ally_code = "299146629"  # Code de test
    
    test_scraper(ally_code)