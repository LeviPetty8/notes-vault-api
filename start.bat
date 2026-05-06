@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo Starting Notes Vault API on http://localhost:3000
python run.py
