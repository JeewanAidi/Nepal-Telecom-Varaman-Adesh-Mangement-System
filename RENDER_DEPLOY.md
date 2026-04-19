# 🇳🇵 Nepal Telecom Travel Order Management System
### Render Deployment Guide — PostgreSQL Production Setup

---

## 🚀 Deploy to Render (Step-by-Step)

### STEP 1 — Push Code to GitHub

First, initialize a Git repo and push to GitHub:

```bash
# In your project folder (VS Code terminal)
git init
git add .
git commit -m "Initial commit - NTC Travel Management System"

# Create a repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/ntc-travel-management.git
git branch -M main
git push -u origin main
```

---

### STEP 2 — Create PostgreSQL Database on Render

1. Go to **https://render.com** → Sign up / Log in
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name:** `ntc-travel-db`
   - **Database:** `ntc_travel`
   - **User:** `ntc_admin`
   - **Region:** `Singapore` (closest to Nepal)
   - **Plan:** Free
4. Click **"Create Database"**
5. Wait ~1 minute for it to spin up
6. Copy the **"Internal Database URL"** — you'll need it next

---

### STEP 3 — Create Web Service on Render

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account → Select your repo
3. Fill in:
   - **Name:** `ntc-travel-management`
   - **Region:** `Singapore`
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn ntc_travel.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan:** Free

---

### STEP 4 — Set Environment Variables on Render

In your Web Service → **"Environment"** tab, add these:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Click **"Generate"** (Render auto-generates) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | Paste the **Internal Database URL** from Step 2 |
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | `YourSecurePassword123!` ← change this! |
| `ADMIN_EMAIL` | `admin@ntc.net.np` |

> ⚠️ **Important:** Set a strong ADMIN_PASSWORD before deploying!

---

### STEP 5 — Deploy

Click **"Create Web Service"** — Render will:
1. Pull your code from GitHub
2. Run `build.sh` (installs packages, collects static, migrates DB, seeds data)
3. Start Gunicorn server

Your app will be live at: `https://ntc-travel-management.onrender.com`

---

### STEP 6 — Login

Go to your Render URL + `/login/`

| Username | Password |
|----------|----------|
| admin | (whatever you set as ADMIN_PASSWORD) |

---

## 🔄 How Auto-Deploy Works

Every time you `git push` to `main`:
1. Render detects the change
2. Runs `build.sh` automatically
3. Restarts the server with new code

---

## 📁 New Files Added for Render

| File | Purpose |
|------|---------|
| `build.sh` | Render build script (install → collectstatic → migrate → seed) |
| `Procfile` | Tells Render how to start Gunicorn |
| `render.yaml` | Infrastructure-as-code (optional) |
| `runtime.txt` | Specifies Python 3.11 |
| `.env.example` | Template for local `.env` file |
| `.gitignore` | Keeps secrets and SQLite out of GitHub |

---

## 💻 Local Development (still works!)

For local development, SQLite is still used automatically (no PostgreSQL needed locally):

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. (Optional) Copy .env.example to .env
copy .env.example .env

# 3. Install updated dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Seed data
python manage.py seed_data

# 6. Run server
python manage.py runserver
```

Local URL: `http://127.0.0.1:8000/login/`
Login: `admin` / `admin123`

---

## 🗄️ Database Logic

```
DATABASE_URL set?  →  YES → PostgreSQL (Render production)
                   →  NO  → SQLite (local development)
```

This is controlled in `settings.py`:
```python
if DATABASE_URL:
    DATABASES = {'default': dj_database_url.config(...)}  # PostgreSQL
else:
    DATABASES = {'default': {'ENGINE': 'sqlite3', ...}}   # SQLite
```

---

## ⚠️ Render Free Tier Limitations

| Limitation | Details |
|-----------|---------|
| Sleep after inactivity | Free web services sleep after 15 min of no traffic. First request takes ~30 seconds. |
| PostgreSQL free tier | 90-day limit, then you must upgrade or recreate |
| Storage | No persistent disk on free tier (media uploads won't persist — use Cloudinary for images if needed) |

**Tip:** Upgrade to **Starter plan ($7/month)** to avoid sleep and get persistent storage.

---

## 🔧 Troubleshooting Render

### Build fails with "Permission denied: ./build.sh"
```bash
# Fix line endings and permissions, then commit:
git update-index --chmod=+x build.sh
git add build.sh
git commit -m "Fix build.sh permissions"
git push
```

### "Application Error" on first load
Check **Render Logs** tab for details. Common causes:
- Missing `DATABASE_URL` environment variable
- Wrong `SECRET_KEY`
- Migration not run yet (usually fixed by redeploying)

### Static files (CSS) not loading
Make sure `whitenoise` is in `requirements.txt` and `STATICFILES_STORAGE` is set correctly in `settings.py`.

---

## 🔐 Security Checklist for Production

- [x] `DEBUG = False` (set via env var)
- [x] Strong `SECRET_KEY` (auto-generated by Render)
- [x] HTTPS enforced (`SECURE_SSL_REDIRECT = True`)
- [x] Secure cookies (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- [x] HSTS headers enabled
- [x] `ALLOWED_HOSTS` restricted to `.onrender.com`
- [ ] Change default `ADMIN_PASSWORD` to something strong!

---

*© 2024 Nepal Telecom Corporation Ltd. — Mahendranagar Branch*
*भ्रमण आदेश व्यवस्थापन प्रणाली | Travel Order Management System*
