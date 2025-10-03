@echo off
REM Script de démarrage pour SWGOH Personal Manager (Windows)

echo ================================================
echo    SWGOH Personal Manager - Demarrage
echo ================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Vérifier si les dépendances sont installées
echo Verification des dependances...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dependances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances
        pause
        exit /b 1
    )
) else (
    echo [OK] Dependances installees
)

echo.
echo ================================================
echo    Demarrage du serveur...
echo ================================================
echo.
echo L'application sera disponible sur:
echo    http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ================================================
echo.

REM Démarrer l'application
python app.py

pause