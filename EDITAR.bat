@echo off
chcp 65001 > nul
title Portfolio — Editor de Conteúdo
cd /d "%~dp0"
python scripts\menu.py
pause
