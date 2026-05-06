#!/bin/bash
set -e
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Starting Notes Vault API on http://localhost:8000"
python run.py
