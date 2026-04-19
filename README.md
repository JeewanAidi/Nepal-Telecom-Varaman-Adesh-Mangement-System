# 🇳🇵 Nepal Telecom Travel Order Management System
### भ्रमण आदेश व्यवस्थापन प्रणाली — Mahendranagar Branch

---

## 📋 Project Overview

A complete web-based Travel Order (भ्रमण आदेश) Management System built for **Nepal Telecom, Mahendranagar Branch** using:

- **Backend:** Django 4.2 (Python)
- **Frontend:** HTML + Bootstrap 5 + Bootstrap Icons
- **Database:** SQLite (default, no setup needed)
- **PDF/Print:** Built-in browser print (official Bhraman Adesh form)

---

## 📁 Project Structure

```
Nepal Telecom Travel Management System/
├── manage.py
├── requirements.txt
├── SETUP.bat               ← One-click Windows setup
├── RUN_SERVER.bat          ← Run server after setup
├── README.md
│
├── ntc_travel/             ← Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── travel_management/      ← Main Django app
    ├── models.py           ← Department, Employee, TravelOrder
    ├── views.py            ← All view functions
    ├── urls.py             ← URL routing
    ├── forms.py            ← Django forms
    ├── admin.py            ← Django admin registration
    ├── apps.py
    ├── management/
    │   └── commands/
    │       └── seed_data.py  ← Seeds demo data
    └── templates/
        ├── base.html
        ├── registration/
        │   └── login.html
        ├── dashboard/
        │   └── dashboard.html
        ├── employees/
        │   ├── employee_list.html
        │   ├── employee_form.html
        │   ├── employee_detail.html
        │   ├── employee_confirm_delete.html
        │   ├── department_list.html
        │   ├── department_form.html
        │   └── department_confirm_delete.html
        └── travel/
            ├── travel_order_list.html
            ├── travel_order_form.html
            ├── travel_order_detail.html
            ├── travel_order_confirm_delete.html
            └── travel_order_print.html  ← Official भ्रमण आदेश form
```

---

## ⚡ QUICK SETUP (Windows — Recommended)

### Option A: One-Click Setup (First Time)

1. Open the project folder in File Explorer
2. **Double-click** `SETUP.bat`
3. Wait for setup to complete (~2 minutes)
4. Browser opens automatically at `http://127.0.0.1:8000/login/`

**Login:** `admin` / `admin123`

### Option B: Run Server (After First Setup)

Double-click `RUN_SERVER.bat` — that's it!

---

## 🛠️ MANUAL SETUP (Step-by-Step)

### Prerequisites
- Python 3.10 or higher: https://python.org/downloads/
- During Python install: ✅ Check "Add Python to PATH"

### Step 1: Open Terminal in Project Folder

```
Right-click in folder → "Open in Terminal"
  OR
Press Win+R → type cmd → cd to project folder
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

```bash
# Windows CMD:
venv\Scripts\activate

# Windows PowerShell:
venv\Scripts\Activate.ps1

# If PowerShell gives an error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Django 4.2
- reportlab (PDF support)
- Pillow (image handling)

### Step 5: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Seed Initial Data

```bash
python manage.py seed_data
```

This creates:
- ✅ Admin user: `admin` / `admin123`
- ✅ 8 departments (Technical, Finance, Customer Service, etc.)
- ✅ 6 sample employees

### Step 7: Start Development Server

```bash
python manage.py runserver
```

### Step 8: Open in Browser

```
http://127.0.0.1:8000/
```

Login with: **admin / admin123**

---

## 🔑 Default Login Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator (full access) |

To create additional users:
```bash
python manage.py createsuperuser
```
Or via Django Admin: `http://127.0.0.1:8000/admin/`

---

## 🌐 URL Reference

| URL | Description |
|-----|-------------|
| `/login/` | Login page |
| `/dashboard/` | Main dashboard |
| `/employees/` | Employee list |
| `/employees/add/` | Add employee |
| `/departments/` | Department list |
| `/travel-orders/` | All travel orders |
| `/travel-orders/create/` | Create new order |
| `/travel-orders/<id>/print/` | Print भ्रमण आदेश |
| `/admin/` | Django admin panel |

---

## ✨ Features

### 🔐 Authentication
- Secure login/logout
- Role-based: Admin (full access) vs. Staff (view only for delete)
- Session management

### 👥 Employee Module
- Add/Edit/Delete employees
- Fields: Employee ID, Name (English + Nepali), Position, Department, Phone, Email
- Active/Inactive status

### 🏢 Department Module
- Create and manage departments
- Employee count per department

### 📋 Travel Order Module (भ्रमण आदेश)
- **Auto-generated Order ID**: NTC-2024-0001 format
- **Auto-fill**: Select employee → position & department auto-fill
- **Date picker** for all date fields
- **Duration calculator**: Auto-calculates trip days
- Status tracking: Pending → Active → Completed / Cancelled
- Quick status update from detail page

### 📊 Dashboard
- Total orders, Active, Completed, Pending, Cancelled counts
- This month's order count
- Recent orders table
- Department-wise statistics with progress bars
- Quick action buttons

### 🔍 Search & Filter
- Search by Order ID, location, employee name
- Filter by employee, department, status
- Filter by date range (from/to)
- Quick status pill filters

### 🖨️ Print / PDF Export
- Official **भ्रमण आदेश** form layout
- Nepal Telecom letterhead style
- Signature sections (Employee, Approving Officer, Branch Head)
- Browser print → Save as PDF using "Save as PDF" printer
- Print button on every order

### ⚙️ CRUD Operations
- ✅ Create travel orders
- ✅ Read/view all orders with full details
- ✅ Update/edit any field
- ✅ Delete (Admin only)

---

## 🔧 Common Issues & Fixes

### Issue: `ModuleNotFoundError: No module named 'django'`
**Fix:** Virtual environment not activated.
```bash
venv\Scripts\activate
```

### Issue: PowerShell says "cannot be loaded because running scripts is disabled"
**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Port 8000 already in use
**Fix:**
```bash
python manage.py runserver 8080
# Then open: http://127.0.0.1:8080/
```

### Issue: `django.db.utils.OperationalError: no such table`
**Fix:** Run migrations again:
```bash
python manage.py migrate
```

### Issue: Static files not loading (CSS broken)
**Fix:** Make sure `DEBUG = True` in settings.py (already set).

---

## 🗄️ Database Reset (Fresh Start)

```bash
# Delete the database
del db.sqlite3

# Run migrations again
python manage.py migrate

# Re-seed data
python manage.py seed_data
```

---

## 📌 Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Web Framework | Django | 4.2.16 |
| Language | Python | 3.10+ |
| Database | SQLite | Built-in |
| Frontend CSS | Bootstrap | 5.3.2 |
| Icons | Bootstrap Icons | 1.11.3 |
| Fonts | Google Fonts (Mukta) | - |
| PDF/Print | Browser Print API | - |

---

## 📞 Support

This system was built for **Nepal Telecom Mahendranagar Branch** internal use.
For technical support, contact your system administrator.

---

*© 2024 Nepal Telecom Corporation Ltd. — Mahendranagar Branch*
*भ्रमण आदेश व्यवस्थापन प्रणाली | Travel Order Management System*
