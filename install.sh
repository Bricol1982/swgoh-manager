#!/bin/bash

echo ""
echo "============================================================"
echo "   INSTALLATION SWGOH MANAGER avec CLOUDSCRAPER"
echo "============================================================"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Vérification Python
echo "🔍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
echo -e "${GREEN}✅ Python trouvé: $PYTHON_VERSION${NC}"

# Installation des dépendances
echo ""
echo "📦 Installation des dépendances..."
echo ""

# cloudscraper
echo "→ Installation de cloudscraper..."
pip3 install cloudscraper --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ cloudscraper installé${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation de cloudscraper${NC}"
    exit 1
fi

# beautifulsoup4
echo "→ Installation de beautifulsoup4..."
pip3 install beautifulsoup4 --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ beautifulsoup4 installé${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation de beautifulsoup4${NC}"
    exit 1
fi

# lxml (parser rapide)
echo "→ Installation de lxml..."
pip3 install lxml --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ lxml installé${NC}"
else
    echo -e "${YELLOW}⚠️  lxml non installé (optionnel)${NC}"
fi

# Autres dépendances
echo "→ Vérification des autres dépendances..."
pip3 install flask pandas requests --quiet

echo ""
echo "============================================================"
echo -e "${GREEN}✅ INSTALLATION TERMINÉE !${NC}"
echo "============================================================"
echo ""
echo "📝 Prochaines étapes :"
echo ""
echo "1. Sauvegardez votre app.py actuel :"
echo "   cp app.py app.py.backup"
echo ""
echo "2. Ajoutez en haut de app.py (après les imports) :"
echo "   import cloudscraper"
echo "   from bs4 import BeautifulSoup"
echo "   import re"
echo ""
echo "3. Remplacez la section API HELPERS dans app.py"
echo "   avec le code fourni"
echo ""
echo "4. Lancez le serveur :"
echo "   python3 app.py"
echo ""
echo "5. Testez avec votre Ally Code dans le navigateur"
echo ""
echo "============================================================"
echo ""