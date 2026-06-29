@echo off
chcp 65001 > nul
title Portfolio — Compilar
cd /d "%~dp0"
echo.
echo  Gerando index.html (PT) e indexEN.html (EN)...
echo.
python scripts\build.py
echo.
echo  Feito! Abra index.html (PT) ou indexEN.html (EN) no navegador.
pause
