#!/usr/bin/env python3
"""
Script pour inspecter la structure de la page SWGOH.gg
et trouver les bons sélecteurs CSS
"""

import cloudscraper
from bs4 import BeautifulSoup
import json
import re

def inspect_page(ally_code):
    """Inspecte la structure de la page"""
    print("\n" + "="*60)
    print("🔍 INSPECTION DE LA PAGE SWGOH.gg")
    print("="*60 + "\n")
    
    scraper = cloudscraper.create_scraper()
    
    # Page des personnages
    url = f"https://swgoh.gg/p/{ally_code}/characters/"
    print(f"📡 URL: {url}\n")
    
    response = scraper.get(url, timeout=20)
    
    if response.status_code != 200:
        print(f"❌ Erreur {response.status_code}")
        return
    
    print("✅ Page récupérée\n")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # === INSPECTION 1 : Scripts JavaScript ===
    print("="*60)
    print("1️⃣  INSPECTION DES SCRIPTS JAVASCRIPT")
    print("="*60)
    
    scripts = soup.find_all('script')
    print(f"📊 {len(scripts)} balises <script> trouvées\n")
    
    for i, script in enumerate(scripts, 1):
        if script.string:
            if 'unitsList' in script.string:
                print(f"✅ Script #{i} contient 'unitsList'")
                print(f"   Longueur: {len(script.string)} caractères")
                
                # Extrait un échantillon
                sample = script.string[:500]
                print(f"   Échantillon:\n{sample}...\n")
                
                # Essaie d'extraire le JSON
                try:
                    match = re.search(r'unitsList\s*=\s*(\[.*?\]);', script.string, re.DOTALL)
                    if match:
                        units_json = json.loads(match.group(1))
                        print(f"   ✅ JSON parsé: {len(units_json)} unités")
                        
                        if units_json:
                            print(f"\n   Exemple d'unité:")
                            print(f"   {json.dumps(units_json[0], indent=2)}")
                except Exception as e:
                    print(f"   ❌ Erreur parsing JSON: {e}")
            
            elif 'character' in script.string.lower() or 'unit' in script.string.lower():
                if len(script.string) > 100:
                    print(f"ℹ️  Script #{i} contient 'character'/'unit'")
                    sample = script.string[:200]
                    print(f"   Échantillon: {sample}...\n")
    
    # === INSPECTION 2 : Structure HTML ===
    print("\n" + "="*60)
    print("2️⃣  INSPECTION DE LA STRUCTURE HTML")
    print("="*60 + "\n")
    
    # Recherche de différentes classes possibles
    selectors = [
        'div.collection-char',
        'div.collection-char-list',
        'div.char-portrait',
        'div.character-card',
        'div.unit-card',
        'div.roster-char',
        'div.character',
        'div[class*="char"]',
        'div[class*="character"]',
        'div[class*="unit"]',
        'div[class*="collection"]'
    ]
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            print(f"✅ Trouvé avec '{selector}': {len(elements)} éléments")
            
            # Affiche le premier élément
            if elements:
                print(f"\n   Premier élément:")
                print(f"   Classes: {elements[0].get('class', [])}")
                print(f"   HTML (tronqué):\n{str(elements[0])[:300]}...\n")
    
    # === INSPECTION 3 : Tables ===
    print("\n" + "="*60)
    print("3️⃣  INSPECTION DES TABLES")
    print("="*60 + "\n")
    
    tables = soup.find_all('table')
    print(f"📊 {len(tables)} tables trouvées\n")
    
    for i, table in enumerate(tables, 1):
        rows = table.find_all('tr')
        print(f"Table #{i}: {len(rows)} lignes")
        if table.get('class'):
            print(f"  Classes: {table.get('class')}")
        
        # Affiche les headers
        headers = table.find_all('th')
        if headers:
            print(f"  Headers: {[h.get_text(strip=True) for h in headers]}")
        
        # Affiche la première ligne
        if rows:
            first_row = rows[0] if not headers else rows[1] if len(rows) > 1 else None
            if first_row:
                cells = first_row.find_all(['td', 'th'])
                print(f"  Première ligne: {len(cells)} cellules")
                print(f"  Contenu: {[c.get_text(strip=True)[:30] for c in cells[:5]]}")
        print()
    
    # === INSPECTION 4 : Recherche de données JSON dans les attributs ===
    print("\n" + "="*60)
    print("4️⃣  RECHERCHE DE DONNÉES JSON DANS LES ATTRIBUTS")
    print("="*60 + "\n")
    
    # Cherche des attributs data-*
    elements_with_data = soup.find_all(attrs=lambda x: x and any(k.startswith('data-') for k in x.keys()))
    
    print(f"📊 {len(elements_with_data)} éléments avec attributs data-*\n")
    
    for elem in elements_with_data[:5]:  # Limite aux 5 premiers
        data_attrs = {k: v for k, v in elem.attrs.items() if k.startswith('data-')}
        if data_attrs:
            print(f"Élément: <{elem.name}>")
            print(f"  Classes: {elem.get('class', [])}")
            print(f"  Attributs data-*:")
            for key, value in data_attrs.items():
                print(f"    {key}: {value[:100] if isinstance(value, str) else value}")
            print()
    
    # === INSPECTION 5 : Sauvegarde de la page ===
    print("\n" + "="*60)
    print("5️⃣  SAUVEGARDE DE LA PAGE")
    print("="*60 + "\n")
    
    filename = f"swgoh_page_{ally_code}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print(f"✅ Page sauvegardée dans: {filename}")
    print(f"   Taille: {len(response.text)} caractères")
    print(f"\n💡 Ouvrez ce fichier dans votre navigateur pour inspecter")
    print(f"   ou utilisez un éditeur pour chercher 'character' ou 'unit'")
    
    # === RÉSUMÉ ===
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    print(f"✅ Scripts trouvés: {len(scripts)}")
    print(f"✅ Tables trouvées: {len(tables)}")
    print(f"✅ Éléments avec data-*: {len(elements_with_data)}")
    print(f"✅ Page sauvegardée: {filename}")
    print("="*60 + "\n")

if __name__ == "__main__":
    import sys
    
    ally_code = sys.argv[1] if len(sys.argv) > 1 else "299146629"
    inspect_page(ally_code)