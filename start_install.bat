@echo off
chcp 65001

cd /d "%~dp0"
python -m venv .venv
call ".venv\Scripts\activate.bat"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

pause
