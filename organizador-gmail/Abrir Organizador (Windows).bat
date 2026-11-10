@echo off
cd /d "%~dp0"
where pythonw >nul 2>nul
if %errorlevel% neq 0 (
  echo No se ha encontrado Python. Instalalo desde https://www.python.org/downloads/
  echo y marca la casilla "Add Python to PATH" durante la instalacion.
  pause
  exit /b
)
start "" pythonw app.py
