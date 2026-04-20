#!/usr/bin/env bash
set -o errexit

echo "============================================"
echo "  NTC Travel Management — Render Build"
echo "============================================"

echo "[1/5] Installing dependencies..."
pip install -r requirements.txt

echo "[2/5] Creating staticfiles directory..."
mkdir -p staticfiles

echo "[3/5] Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "[4/5] Running database migrations..."
python manage.py migrate

echo "[5/5] Seeding initial data..."
python manage.py seed_data

echo ""
echo "============================================"
echo "  Build complete!"
echo "============================================"
