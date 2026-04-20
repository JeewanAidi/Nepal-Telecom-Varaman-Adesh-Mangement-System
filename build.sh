#!/usr/bin/env bash
set -o errexit

echo "============================================"
echo "  NTC Travel Management — Render Build"
echo "============================================"

echo "[1/6] Installing dependencies..."
pip install -r requirements.txt

echo "[2/6] Creating staticfiles directory..."
mkdir -p staticfiles

echo "[3/6] Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "[4/6] Making migrations..."
python manage.py makemigrations

echo "[5/6] Running database migrations..."
python manage.py migrate

echo "[6/6] Seeding initial data..."
python manage.py seed_data

echo ""
echo "============================================"
echo "  Build complete!"
echo "============================================"
