import cloudscraper
from bs4 import BeautifulSoup
import re

scraper = cloudscraper.create_scraper()
response = scraper.get("https://swgoh.gg/p/299146629/characters/")

soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('div', class_='unit-card')

print(f"Nombre de cartes: {len(cards)}\n")

if cards:
    print("=" * 60)
    print("PREMIÈRE CARTE (extrait):")
    print("=" * 60)
    card = cards[0]
    
    # Classes de la carte
    print(f"Classes: {card.get('class')}")
    
    # Recherche du nom
    img = card.find('img')
    if img:
        print(f"Image alt: {img.get('alt')}")
        print(f"Image src: {img.get('src')}")
    
    # Liens
    links = card.find_all('a')
    for link in links:
        print(f"Lien href: {link.get('href')}")
    
    # Tout le texte
    print(f"\nTexte complet: {card.get_text()[:200]}")
    
    # Structure HTML (premier niveau)
    print("\nEnfants directs:")
    for child in card.children:
        if child.name:
            print(f"  - {child.name} (classes: {child.get('class')})")
    
    print("\n" + "=" * 60)
    print("HTML COMPLET DE LA PREMIÈRE CARTE:")
    print("=" * 60)
    print(card.prettify()[:1000])
