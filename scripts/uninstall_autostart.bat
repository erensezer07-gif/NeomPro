@echo off
REM Neom Asistan otomatik baslatmayi kaldir
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0uninstall_autostart.ps1"
pause
