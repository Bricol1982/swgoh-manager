#!/bin/bash
# Script de démarrage pour SWGOH Personal Manager (Mac/Linux)

echo "================================================"
echo "   SWGOH Personal Manager - Démarrage"
echo "================================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé"
    echo "Installez Python depuis https://www.python.org/"
    exit 1
fi

echo "[OK] Python détecté: $(python3 --version)"
echo ""

# Vérifier si les dépendances sont installées
echo "Vérification des dépendances..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "[INFO] Installation des dépendances..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERREUR] Échec de l'installation des dépendances"
        exit 1
    fi
else
    echo "[OK] Dépendances installées"
fi

echo ""
echo "================================================"
echo "   Démarrage du serveur..."
echo "================================================"
echo ""
echo "L'application sera disponible sur:"
echo "   http://localhost:5000"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo "================================================"
echo ""

# Démarrer l'application
python3 app.py