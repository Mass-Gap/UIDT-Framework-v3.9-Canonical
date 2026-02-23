@echo off
echo ========================================================
echo UIDT Framework Auto-Updater
echo ========================================================
cd /d "C:\Users\badbu\Documents\github\UIDT-Framework-V3.9"

echo Checking for updates from GitHub...
git pull --rebase --autostash origin main

echo ========================================================
echo Sync Complete.
timeout /t 5
