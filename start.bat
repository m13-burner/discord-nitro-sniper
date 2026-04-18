@echo off
color 0b
title Nitro Sniper V1
echo Installing requirements...
pip install -r requirements.txt >nul 2>&1
echo Starting Sniper...
python sniper.py
pause
