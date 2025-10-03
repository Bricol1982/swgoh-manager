#!/usr/bin/env python3
"""
Patch automatique pour ajouter les nouvelles fonctions de parsing
"""

import os
import shutil
from datetime import datetime

NEW_FUNCTIONS = '''
def parse_character_roster(html):
    """Parse le roster de personnages depuis la page HTML - Version finale"""
    soup = BeautifulSoup(html, 'html.parser')
    roster = []
    
    try:
        print("🔍 Recherche des cartes de personnages...")
        
        # La nouvelle structure utilise div.unit-card
        unit_cards = soup.find_all('div', class_='unit-card')
        print(f"✅ {len(unit_cards)} unit-cards trouvées")
        
        for card in unit_cards:
            try:
                character = parse_unit_card(card)
                if character:
                    roster.append(character)
            except Exception as e:
                continue
        
        if roster:
            print(f"✅ {len(roster)} personnages extraits avec succès")
        else:
            print("⚠️  Aucun personnage extrait")
        
    except Exception as e:
        print(f"❌ Erreur parsing roster: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return roster

def parse_unit_card(card):
    """Parse une unit-card (nouvelle structure SWGOH.gg)"""
    try:
        # === NOM DU PERSONNAGE ===
        name = "Unknown"
        img = card.find('img', class_='character-portrait__img')
        if img and img.get('alt'):
            name = img['alt'].strip()
        
        if name == "Unknown":
            link = card.find('a', href=re.compile(r'/characters/'))
            if link:
                match = re.search(r'/characters/([^/]+)/', link.get('href', ''))
                if match:
                    name = match.group(1).replace('-', ' ').title()
        
        # === BASE ID ===
        base_id = ""
        link = card.find('a', href=re.compile(r'/characters/'))
        if link:
            match = re.search(r'/characters/([^/]+)/', link['href'])
            if match:
                base_id = match.group(1).upper().replace('-', '')
        
        if not base_id:
            base_id = name.upper().replace(' ', '').replace("'", '').replace('-', '')
        
        # === GEAR LEVEL ===
        gear_level = 1
        gear_elem = card.find('div', class_=re.compile(r'.*gear.*', re.I))
        if gear_elem:
            text = gear_elem.get_text(strip=True)
            gear_match = re.search(r'(\\\\d+)', text)
            if gear_match:
                gear_level = int(gear_match.group(1))
        
        if gear_level == 1:
            for class_name in card.get('class', []):
                if 'gear' in class_name.lower():
                    gear_match = re.search(r'(\\\\d+)', class_name)
                    if gear_match:
                        gear_level = int(gear_match.group(1))
                        break
        
        # === RELIC TIER ===
        relic_tier = 0
        for class_name in card.get('class', []):
            if 'tier' in class_name.lower() or 'relic' in class_name.lower():
                tier_match = re.search(r'(\\\\d+)', class_name)
                if tier_match:
                    relic_tier = int(tier_match.group(1))
                    break
        
        if relic_tier == 0:
            relic_elem = card.find(class_=re.compile(r'.*tier.*|.*relic.*', re.I))
            if relic_elem:
                text = relic_elem.get_text(strip=True)
                relic_match = re.search(r'(\\\\d+)', text)
                if relic_match:
                    relic_tier = int(relic_match.group(1))
        
        # === GALACTIC POWER ===
        power = 0
        all_text = card.get_text()
        power_matches = re.findall(r'(\\\\d{1,3}(?:,\\\\d{3})+|\\\\d{4,})', all_text)
        if power_matches:
            powers = [int(p.replace(',', '')) for p in power_matches]
            power = max(powers) if powers else 0
        
        # === FLAGS ===
        is_gl = 'galactic-legend' in ' '.join(card.get('class', [])).lower()
        has_ultimate = 'ultimate' in ' '.join(card.get('class', [])).lower()
        
        if name and name != "Unknown" and len(name) > 1:
            character = {
                'base_id': base_id,
                'name': name,
                'level': 85,
                'gear_level': gear_level,
                'relic_tier': relic_tier,
                'power': power,
                'galactic_power': power,
                'combat_type': 1,
                'has_ultimate': has_ultimate,
                'mods': []
            }
            return character
        
        return None
        
    except Exception as e:
        return None
'''

def main():
    print("\n" + "="*60)
    print("🔧 PATCH AUTOMATIQUE - Ajout des fonctions de parsing")
    print("="*60 + "\n")
    
    if not os.path.exists('app.py'):
        print("❌ Fichier app.py non trouvé")
        return False
    
    # Sauvegarde
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = f"app.py.backup_{timestamp}"
    shutil.copy2('app.py', backup)
    print(f"✅ Sauvegarde créée: {backup}")
    
    # Lecture
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouve l'endroit où insérer
    marker = "# ==================== OPTIMISATION ===================="
    
    if marker not in content:
        print("❌ Marqueur OPTIMISATION non trouvé")
        print("   Ajoutez manuellement les fonctions avant la section OPTIMISATION")
        return False
    
    # Vérifie si parse_unit_card existe déjà
    if 'def parse_unit_card(' in content:
        print("ℹ️  parse_unit_card existe déjà")
        response = input("Remplacer quand même ? (o/N): ")
        if response.lower() != 'o':
            print("❌ Opération annulée")
            return False
        
        # Supprime l'ancienne version
        # Trouve le début de parse_unit_card
        start = content.find('def parse_unit_card(')
        if start != -1:
            # Trouve la prochaine fonction ou le marqueur OPTIMISATION
            end = content.find('\\ndef ', start + 1)
            if end == -1:
                end = content.find(marker, start)
            
            if end != -1:
                content = content[:start] + content[end:]
                print("✅ Ancienne version supprimée")
    
    # Supprime aussi parse_character_roster si elle existe
    if 'def parse_character_roster(' in content:
        start = content.find('def parse_character_roster(')
        if start != -1:
            end = content.find('\\ndef ', start + 1)
            if end == -1:
                end = content.find(marker, start)
            
            if end != -1:
                content = content[:start] + content[end:]
                print("✅ Ancienne parse_character_roster supprimée")
    
    # Insère les nouvelles fonctions
    insert_pos = content.find(marker)
    content = content[:insert_pos] + NEW_FUNCTIONS + '\\n' + content[insert_pos:]
    
    # Sauvegarde
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ PATCH APPLIQUÉ AVEC SUCCÈS !")
    print("\n📝 Prochaines étapes :")
    print("   1. python3 test_parser.py 299146629")
    print("   2. python3 app.py")
    print("   3. Testez dans le navigateur")
    print("\n💡 En cas de problème:")
    print(f"   cp {backup} app.py")
    print("\n" + "="*60 + "\n")
    
    return True

if __name__ == "__main__":
    main()