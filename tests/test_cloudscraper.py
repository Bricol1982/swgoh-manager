#!/usr/bin/env python3
"""
Script de test rapide pour vérifier que cloudscraper fonctionne
"""

import sys

def test_import():
    """Test l'import de cloudscraper"""
    print("\n" + "="*60)
    print("TEST 1 : Import des bibliothèques")
    print("="*60)
    
    try:
        import cloudscraper
        print("✅ cloudscraper importé")
    except ImportError:
        print("❌ cloudscraper non trouvé")
        print("   Installez-le avec: pip3 install cloudscraper")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 importé")
    except ImportError:
        print("❌ beautifulsoup4 non trouvé")
        print("   Installez-le avec: pip3 install beautifulsoup4")
        return False
    
    return True

def test_swgoh_gg(ally_code="299146629"):
    """Test la connexion à SWGOH.gg"""
    print("\n" + "="*60)
    print(f"TEST 2 : Connexion à SWGOH.gg")
    print("="*60)
    
    try:
        import cloudscraper
        from bs4 import BeautifulSoup
        import re
        
        # Création du scraper
        print(f"🔧 Création du scraper cloudscraper...")
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        # Test de connexion
        url = f"https://swgoh.gg/p/{ally_code}/"
        print(f"📡 Connexion à: {url}")
        print(f"⏳ Patientez...")
        
        response = scraper.get(url, timeout=20)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Connexion réussie !")
            
            # Parse la page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraction du nom
            name_elem = soup.find('h5', class_='pull-left')
            if name_elem:
                player_name = name_elem.get_text(strip=True)
                print(f"👤 Joueur trouvé: {player_name}")
            
            # Extraction de la guilde
            guild_elem = soup.find('a', href=re.compile(r'/g/'))
            if guild_elem:
                guild_name = guild_elem.get_text(strip=True)
                print(f"🏰 Guilde: {guild_name}")
            
            # Extraction du GP
            stats_divs = soup.find_all('div', class_='profile-stat')
            for stat_div in stats_divs:
                label_div = stat_div.find('div', class_='stat-label')
                value_div = stat_div.find('div', class_='stat-value')
                
                if label_div and value_div:
                    label = label_div.get_text(strip=True)
                    value = value_div.get_text(strip=True)
                    
                    if 'Galactic Power' in label:
                        print(f"⚡ {label}: {value}")
            
            print("\n✅ Tous les tests passés ! Cloudscraper fonctionne parfaitement.")
            return True
            
        elif response.status_code == 403:
            print("❌ Erreur 403 - Protection Cloudflare active")
            print("   Cela ne devrait pas arriver avec cloudscraper...")
            return False
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_roster(ally_code="299146629"):
    """Test la récupération du roster"""
    print("\n" + "="*60)
    print(f"TEST 3 : Récupération du roster")
    print("="*60)
    
    try:
        import cloudscraper
        from bs4 import BeautifulSoup
        import json
        import re
        
        scraper = cloudscraper.create_scraper()
        url = f"https://swgoh.gg/p/{ally_code}/characters/"
        
        print(f"📡 Connexion à: {url}")
        response = scraper.get(url, timeout=20)
        
        if response.status_code == 200:
            print("✅ Page roster récupérée")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Recherche du JSON
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'unitsList' in script.string:
                    match = re.search(r'unitsList\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                    if match:
                        units_data = json.loads(match.group(1))
                        
                        # Compte les personnages
                        characters = [u for u in units_data if u.get('combat_type') == 1]
                        print(f"✅ {len(characters)} personnages trouvés !")
                        
                        # Affiche les 5 meilleurs
                        sorted_chars = sorted(characters, key=lambda x: x.get('power', 0), reverse=True)
                        print(f"\n🏆 Top 5 personnages :")
                        for i, char in enumerate(sorted_chars[:5], 1):
                            name = char.get('name', 'Unknown')
                            gear = char.get('gear_level', 0)
                            relic = char.get('relic_tier', 0)
                            power = char.get('power', 0)
                            print(f"   {i}. {name} - G{gear} R{max(0, relic-2)} - {power:,} GP")
                        
                        return True
            
            print("⚠️  JSON non trouvé, essai avec parsing HTML...")
            char_cards = soup.find_all('div', class_='collection-char')
            print(f"✅ {len(char_cards)} cartes de personnages trouvées")
            return len(char_cards) > 0
            
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("🧪 TEST DE CLOUDSCRAPER POUR SWGOH.gg")
    print("="*60)
    
    # Ally code à tester
    if len(sys.argv) > 1:
        ally_code = sys.argv[1].replace('-', '')
    else:
        ally_code = "299146629"
    
    print(f"\n📝 Ally Code testé: {ally_code}")
    
    # Tests
    results = []
    
    # Test 1: Imports
    results.append(test_import())
    
    if results[0]:
        # Test 2: Connexion
        results.append(test_swgoh_gg(ally_code))
        
        if results[1]:
            # Test 3: Roster
            results.append(test_roster(ally_code))
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    test_names = ["Import des bibliothèques", "Connexion SWGOH.gg", "Récupération du roster"]
    
    for i, (name, result) in enumerate(zip(test_names[:len(results)], results)):
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{i+1}. {name}: {status}")
    
    print("="*60)
    
    if all(results):
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("\n✅ Cloudscraper fonctionne parfaitement.")
        print("✅ Vous pouvez maintenant intégrer le code dans app.py")
        print("\n📝 Instructions :")
        print("   1. Ouvrez app.py")
        print("   2. Ajoutez les imports en haut du fichier")
        print("   3. Remplacez la section API HELPERS")
        print("   4. Lancez: python3 app.py")
        print("   5. Testez avec votre Ally Code")
    else:
        print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("\n💡 Solutions possibles :")
        if not results[0]:
            print("   → Installez les dépendances: pip3 install cloudscraper beautifulsoup4")
        else:
            print("   → Vérifiez votre connexion Internet")
            print("   → Vérifiez que l'Ally Code est valide")
            print("   → Réessayez dans quelques minutes")
    
    print("\n" + "="*60 + "\n")
    
    return all(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)