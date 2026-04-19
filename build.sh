#!/usr/bin/env bash
# build.sh — Render build script
# Render runs this automatically on every deployment.
# Make sure this file uses LF line endings (not CRLF).

set -o errexit   # Exit immediately if any command fails

echo "============================================"
echo "  NTC Travel Management — Render Build"
echo "============================================"

# 1. Install Python dependencies
echo "[1/4] Installing dependencies..."
pip install -r requirements.txt

# 2. Collect static files (WhiteNoise will serve them)
echo "[2/4] Collecting static files..."
python manage.py collectstatic --no-input

# 3. Run database migrations
echo "[3/4] Running database migrations..."
python manage.py migrate

# 4. Seed initial data (admin user + departments + sample employees)
#    The seed_data command is idempotent — safe to run on every deploy.
echo "[4/4] Seeding initial data..."
python manage.py seed_data

echo ""
echo "============================================"
echo "  Build complete! Render will start Gunicorn."
echo "============================================"
