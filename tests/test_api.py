"""
Script de diagnostic pour tester l'API et identifier les problèmes
"""

import requests
import json

def test_swgoh_gg_api(ally_code):
    """Test l'API SWGOH.gg"""
    clean_code = ally_code.replace('-', '')
    url = f"https://swgoh.gg/api/player/{clean_code}/"
    
    print(f"\n{'='*60}")
    print(f"Test API SWGOH.gg")
    print(f"{'='*60}")
    print(f"URL: {url}")
    print(f"Ally Code: {clean_code}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ API accessible!")
            print(f"\nStructure des données reçues:")
            print(json.dumps(data, indent=2)[:500] + "...")
            return True, data
        else:
            print(f"\n✗ Erreur HTTP {response.status_code}")
            print(f"Réponse: {response.text[:200]}")
            return False, None
            
    except requests.exceptions.Timeout:
        print("\n✗ Timeout - L'API ne répond pas")
        return False, None
    except requests.exceptions.ConnectionError:
        print("\n✗ Erreur de connexion - Impossible de joindre l'API")
        return False, None
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {str(e)}")
        return False, None

def test_alternative_api(ally_code):
    """Test une API alternative"""
    clean_code = ally_code.replace('-', '')
    
    # Essai avec swgoh.help (nécessite authentification)
    print(f"\n{'='*60}")
    print(f"Test API alternative (swgoh.help)")
    print(f"{'='*60}")
    print("Note: Cette API nécessite une authentification")
    
    # Pour l'instant, juste informatif
    print("URL: https://api.swgoh.help/swgoh")
    print("Documentation: https://api.swgoh.help/")

def test_database_connection():
    """Test la connexion à la base de données"""
    import sqlite3
    
    print(f"\n{'='*60}")
    print(f"Test Base de données")
    print(f"{'='*60}")
    
    try:
        conn = sqlite3.connect('swgoh_data.db')
        c = conn.cursor()
        
        # Vérifie les tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = c.fetchall()
        
        print(f"✓ Base de données accessible")
        print(f"Tables présentes: {[t[0] for t in tables]}")
        
        # Vérifie les données existantes
        c.execute("SELECT COUNT(*) FROM player_info")
        player_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM characters")
        char_count = c.fetchone()[0]
        
        print(f"\nDonnées existantes:")
        print(f"  - Joueurs: {player_count}")
        print(f"  - Personnages: {char_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"✗ Erreur base de données: {str(e)}")
        return False

def check_frontend_connection():
    """Vérifie si le frontend peut se connecter au backend"""
    print(f"\n{'='*60}")
    print(f"Test Connexion Frontend/Backend")
    print(f"{'='*60}")
    
    try:
        # Test endpoint de vérification
        response = requests.get('http://localhost:5000/api/check_loaded_data', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Backend accessible")
            print(f"Données chargées: {data.get('has_data', False)}")
            return True
        else:
            print(f"✗ Backend répond avec erreur: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Backend non accessible - Le serveur Flask est-il démarré?")
        print("   Lancez: python app.py")
        return False
    except Exception as e:
        print(f"✗ Erreur: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("DIAGNOSTIC SWGOH PERSONAL MANAGER")
    print("="*60)
    
    # Test 1: Base de données
    db_ok = test_database_connection()
    
    # Test 2: Backend
    backend_ok = check_frontend_connection()
    
    # Test 3: API avec un ally code de test
    test_ally_code = "299146629"  # Remplacez par votre vrai ally code
    api_ok, data = test_swgoh_gg_api(test_ally_code)
    
    # Test 4: API alternative
    test_alternative_api(test_ally_code)
    
    # Résumé
    print(f"\n{'='*60}")
    print("RÉSUMÉ")
    print(f"{'='*60}")
    print(f"Base de données: {'✓ OK' if db_ok else '✗ Problème'}")
    print(f"Backend Flask: {'✓ OK' if backend_ok else '✗ Problème'}")
    print(f"API SWGOH.gg: {'✓ OK' if api_ok else '✗ Problème'}")
    
    if not api_ok:
        print(f"\n⚠ RECOMMANDATION:")
        print("L'API SWGOH.gg semble indisponible ou avoir changé.")
        print("Solutions possibles:")
        print("1. Utiliser les données de démonstration (déjà implémenté)")
        print("2. Créer un compte sur https://api.swgoh.help/")
        print("3. Importer les données manuellement")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()