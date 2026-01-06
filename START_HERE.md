# 🚀 START HERE - Complete Setup Guide

Welcome to the University Document Management System! Follow these steps to get started.

## ⚡ Quick Start (For Experienced Developers)

```bash
# 1. Database
createdb university_docs

# 2. Backend
cd server
python -m venv venv
venv\Scripts\activate  # Windows | source venv/bin/activate (Linux/Mac)
pip install -r requirements.txt
copy .env.example .env  # Edit with your settings
python main.py

# 3. Frontend (new terminal)
cd client
npm install
copy .env.local.example .env.local
npm run dev

# 4. Open http://localhost:3000
```

---

## 📚 Detailed Setup (First Time Users)

### Choose Your Path:

#### 🤖 **Option A: Automated Setup (Easiest)**
Perfect if you want to get running quickly with minimal configuration.

**Windows:**
```bash
cd server
setup.bat
```

**Linux/Mac:**
```bash
cd server
chmod +x setup.sh
./setup.sh
```

Then follow the on-screen instructions!

---

#### 🛠️ **Option B: Manual Setup (Recommended)**
Perfect if you want to understand each step.

**Follow this guide:** [INSTALLATION_CHECKLIST.md](INSTALLATION_CHECKLIST.md)

This comprehensive checklist walks you through:
- ✅ Prerequisites verification
- ✅ Backend setup (step-by-step)
- ✅ Database configuration
- ✅ Frontend setup
- ✅ Testing the system
- ✅ Troubleshooting

---

#### 📖 **Option C: Quick Reference**
Perfect if you just need a reminder of the commands.

**See:** [QUICKSTART.md](QUICKSTART.md) - 5-minute setup guide

---

## 🎯 What to Read Based on Your Needs

### "I want to install and run locally"
1. **Start:** [INSTALLATION_CHECKLIST.md](INSTALLATION_CHECKLIST.md)
2. **Troubleshooting:** [COMMON_ISSUES.md](COMMON_ISSUES.md)
3. **Details:** [README.md](README.md)

### "I want to deploy to production"
1. **Start:** [DEPLOYMENT.md](DEPLOYMENT.md)
2. **Backend:** [server/README.md](server/README.md)
3. **Frontend:** [client/README.md](client/README.md)

### "I want to understand the system"
1. **Overview:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
2. **Full docs:** [README.md](README.md)
3. **API:** http://localhost:8000/docs (after starting backend)

### "I'm getting errors"
1. **Common issues:** [COMMON_ISSUES.md](COMMON_ISSUES.md)
2. **Backend setup:** [server/INSTALLATION.md](server/INSTALLATION.md)
3. **Troubleshooting:** Check README.md troubleshooting section

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] **Python 3.9+** - Check: `python --version`
- [ ] **Node.js 18+** - Check: `node --version`
- [ ] **PostgreSQL 12+** - Check: `psql --version`
- [ ] **Tesseract OCR** - Check: `tesseract --version`
  - Windows: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)
  - Ubuntu: `sudo apt-get install tesseract-ocr`
  - Mac: `brew install tesseract`

**Don't have these?** Each can be installed quickly:
- Python: https://python.org
- Node.js: https://nodejs.org
- PostgreSQL: https://postgresql.org
- Tesseract: See links above

---

## 🎬 Your First Session

### Step 1: Install (Choose A, B, or C above)

### Step 2: Start Backend
```bash
cd server
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
python main.py
```

✅ **Success:** You'll see "Uvicorn running on http://0.0.0.0:8000"

### Step 3: Start Frontend (New Terminal)
```bash
cd client
npm run dev
```

✅ **Success:** You'll see "Local: http://localhost:3000"

### Step 4: Test
1. Open http://localhost:3000
2. You should see the dashboard
3. Try uploading a document

---

## ❓ Common First-Time Questions

### Q: Which guide should I follow?
**A:** If first time, use [INSTALLATION_CHECKLIST.md](INSTALLATION_CHECKLIST.md) - it's the most comprehensive.

### Q: Do I need to install Tesseract?
**A:** Yes, for OCR features. The system will run without it, but won't extract text from documents.

### Q: Can I skip PostgreSQL and use SQLite?
**A:** Technically yes (edit `config.py`), but PostgreSQL is recommended for production and handles 5000+ records better.

### Q: What if I get errors during installation?
**A:** Check [COMMON_ISSUES.md](COMMON_ISSUES.md) - it covers 90% of common problems.

### Q: How do I stop the servers?
**A:** Press `Ctrl+C` in each terminal (backend and frontend).

### Q: Where are uploaded files stored?
**A:** In `server/uploads/` directory, organized by student ID.

---

## 🏗️ Project Structure Overview

```
document_reader/
├── 📚 Documentation Files
│   ├── START_HERE.md (this file)
│   ├── QUICKSTART.md
│   ├── INSTALLATION_CHECKLIST.md
│   ├── DEPLOYMENT.md
│   ├── COMMON_ISSUES.md
│   └── README.md
│
├── 🔧 Backend (server/)
│   ├── main.py - FastAPI application
│   ├── models.py - Database models
│   ├── services/ - OCR and Excel services
│   └── setup.bat/setup.sh - Setup scripts
│
└── 💻 Frontend (client/)
    ├── app/ - Next.js pages
    ├── lib/api.ts - API client
    └── package.json - Dependencies
```

---

## 🎓 Learning Path

### Day 1: Setup
1. Follow installation guide
2. Get both servers running
3. Upload your first document

### Day 2: Explore
1. Try all features (upload, search, export)
2. Read API docs: http://localhost:8000/docs
3. Review code structure

### Day 3: Customize
1. Modify UI colors/styling
2. Add custom fields
3. Adjust OCR patterns

### Day 4: Deploy
1. Follow [DEPLOYMENT.md](DEPLOYMENT.md)
2. Deploy to Vercel
3. Set up production database

---

## 📞 Need Help?

### During Installation
→ [COMMON_ISSUES.md](COMMON_ISSUES.md)

### Backend Problems
→ [server/INSTALLATION.md](server/INSTALLATION.md)

### Understanding the System
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### Deployment
→ [DEPLOYMENT.md](DEPLOYMENT.md)

### Everything Else
→ [README.md](README.md)

---

## ✨ What You'll Build

A complete system that:
- 📤 Uploads student documents via camera or file
- 🔍 Extracts student data automatically (OCR)
- 📸 Detects and saves student photos
- 💾 Stores everything in PostgreSQL
- 🔎 Searches 5000+ students instantly
- 📊 Exports data to Excel
- 🎨 Beautiful, responsive UI
- ☁️ Ready for Vercel deployment

---

## 🚀 Ready to Start?

Pick your installation method above and begin!

**Recommended order:**
1. Read this file (you're here! ✅)
2. Check prerequisites
3. Follow [INSTALLATION_CHECKLIST.md](INSTALLATION_CHECKLIST.md)
4. Keep [COMMON_ISSUES.md](COMMON_ISSUES.md) handy
5. Have fun! 🎉

---

**Pro Tip:** Keep all terminals open while developing. You'll need:
- Terminal 1: Backend (`python main.py`)
- Terminal 2: Frontend (`npm run dev`)
- Terminal 3: Commands (git, database, etc.)

Good luck! 🍀
