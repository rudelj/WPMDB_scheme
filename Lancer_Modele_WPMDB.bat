@echo off
title Visualiseur de Modele de Donnees WPMDB (super-er-diagram)
cd /d "%~dp0\viewer"
echo =====================================================================
echo  Lancement du Visualiseur Interactif super-er-diagram pour WPMDB
echo =====================================================================
echo  - 113 Tables
echo  - 64 Relations Clés Etrangeres
echo  - 7 Domaines Metier (Work Items, Schedules, Mandates, NSO...)
echo.
echo Ouverture dans votre navigateur par defaut...
start "" "index.html"
echo.
pause
