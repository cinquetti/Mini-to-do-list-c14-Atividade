#!/usr/bin/env bash
set -e

echo "=== Criando ambiente virtual ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Instalando dependências ==="
pip install -U pip setuptools wheel
pip install -r requirements.txt

echo "=== Construindo pacote instalável ==="
python3 -m build

echo "=== Gerando executável standalone ==="
pip install pyinstaller
pyinstaller --onefile run.py --name todo-flask

echo "Build finalizado!"
echo "Executável disponível em: dist/todo-flask"
