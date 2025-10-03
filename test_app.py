"""
Script de test pour vérifier l'installation de SWGOH Manager
"""

import sys
import os

def test_python_version():
    """Vérifie la version de Python"""
    print("🐍 Test de la version Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} OK")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} - Version 3.8+ requise")
        return False

def test_imports():
    """Teste l'import des modules requis"""
    print("\n📦 Test des dépendances...")
    modules = {
        'flask': 'Flask',
        'requests': 'Requests',
        'pandas': 'Pandas',
        'sqlite3': 'SQLite3 (inclus)',
        'dotenv': 'python-dotenv'
    }
    
    all_ok = True
    for module, name in modules.items():
        try:
            if module == 'dotenv':
                __import__('dotenv')
            else:
                __import__(module)
            print(f"   ✓ {name} installé")
        except ImportError:
            print(f"   ✗ {name} MANQUANT")
            all_ok = False
    
    return all_ok

def test_file_structure():
    """Vérifie la structure des fichiers"""
    print("\n📁 Test de la structure des fichiers...")
    required_files = {
        'app.py': 'Application principale',
        'requirements.txt': 'Liste des dépendances',
        'templates/base.html': 'Template de base',
        'templates/index.html': 'Page Dashboard',
        'templates/mods.html': 'Page Mods',
        'templates/optimizer.html': 'Page Optimizer',
        'templates/loadouts.html': 'Page Loadouts',
        'templates/gac.html': 'Page GAC'
    }
    
    all_ok = True
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"   ✓ {file} - {description}")
        else:
            print(f"   ✗ {file} MANQUANT - {description}")
            all_ok = False
    
    return all_ok

def test_database():
    """Teste la création de la base de données"""
    print("\n💾 Test de la base de données...")
    try:
        import sqlite3
        
        # Supprime la DB de test si elle existe
        test_db = 'test_swgoh.db'
        if os.path.exists(test_db):
            os.remove(test_db)
        
        # Crée une DB de test
        conn = sqlite3.connect(test_db)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS test_table (
            id INTEGER PRIMARY KEY,
            data TEXT
        )''')
        
        c.execute("INSERT INTO test_table (data) VALUES ('test')")
        conn.commit()
        
        c.execute("SELECT * FROM test_table")
        result = c.fetchone()
        
        conn.close()
        os.remove(test_db)
        
        if result:
            print("   ✓ Création et opérations SQLite OK")
            return True
        else:
            print("   ✗ Erreur lors des opérations SQLite")
            return False
            
    except Exception as e:
        print(f"   ✗ Erreur SQLite: {e}")
        return False

def test_flask_app():
    """Teste le démarrage de Flask"""
    print("\n🌐 Test de l'application Flask...")
    try:
        # Import le module app
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Ne pas exécuter l'app, juste l'importer
        import app as flask_app
        
        if hasattr(flask_app, 'app'):
            print("   ✓ Application Flask initialisée")
            
            # Teste quelques routes
            test_client = flask_app.app.test_client()
            
            routes_to_test = [
                ('/', 'Dashboard'),
                ('/mods', 'Mods'),
                ('/optimizer', 'Optimizer'),
                ('/loadouts', 'Loadouts'),
                ('/gac', 'GAC')
            ]
            
            for route, name in routes_to_test:
                response = test_client.get(route)
                if response.status_code == 200:
                    print(f"   ✓ Route {route} ({name}) accessible")
                else:
                    print(f"   ✗ Route {route} ({name}) erreur {response.status_code}")
                    return False
            
            return True
        else:
            print("   ✗ L'application Flask n'est pas correctement initialisée")
            return False
            
    except Exception as e:
        print(f"   ✗ Erreur lors du test Flask: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=" * 60)
    print("🧪 SWGOH Manager - Tests de Vérification")
    print("=" * 60)
    
    results = []
    
    # Exécute tous les tests
    results.append(("Version Python", test_python_version()))
    results.append(("Dépendances", test_imports()))
    results.append(("Structure fichiers", test_file_structure()))
    results.append(("Base de données", test_database()))
    results.append(("Application Flask", test_flask_app()))
    
    # Affiche le résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ RÉUSSI" if passed else "✗ ÉCHOUÉ"
        print(f"{test_name:<25} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n🎉 Tous les tests sont passés !")
        print("✅ Votre installation est correcte.")
        print("\n💡 Vous pouvez maintenant lancer l'application avec:")
        print("   python app.py")
        print("\n   Ou utilisez les scripts de lancement:")
        print("   - Windows: run.bat")
        print("   - Linux/Mac: ./run.sh")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("❌ Vérifiez les erreurs ci-dessus et:")
        print("   1. Installez les dépendances manquantes: pip install -r requirements.txt")
        print("   2. Vérifiez que tous les fichiers sont présents")
        print("   3. Relancez ce script de test")
        return 1

if __name__ == '__main__':
    sys.exit(main())