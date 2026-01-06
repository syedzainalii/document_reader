# Quick Start Guide - 5 Minutes Setup

Get the University Document Management System running locally in 5 minutes.

## Prerequisites Check

✅ Node.js 18+ installed: `node --version`
✅ Python 3.9+ installed: `python --version`
✅ PostgreSQL installed: `psql --version`
✅ Tesseract OCR installed: `tesseract --version`

## Step 1: Database Setup (1 minute)

```bash
# Create database
createdb university_docs

# Or using psql:
psql -U postgres -c "CREATE DATABASE university_docs;"
```

## Step 2: Backend Setup (2 minutes)

```bash
cd server

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/university_docs" > .env
echo "ALLOWED_ORIGINS=http://localhost:3000" >> .env

# Start backend
python main.py
```

✅ Backend running at http://localhost:8000

## Step 3: Frontend Setup (2 minutes)

**New terminal:**

```bash
cd client

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start frontend
npm run dev
```

✅ Frontend running at http://localhost:3000

## Step 4: Test the System

Open browser: http://localhost:3000

1. ✅ Dashboard loads
2. ✅ Go to Upload page
3. ✅ Upload a student ID card
4. ✅ View extracted data
5. ✅ Check Students page
6. ✅ Export to Excel

## Common Issues

### Tesseract Not Found

**Windows:**
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to .env:
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Mac:**
```bash
brew install tesseract
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
# Windows:
pg_ctl status

# Linux/Mac:
sudo service postgresql status

# Update .env with correct credentials
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/university_docs
```

### Port Already in Use

```bash
# Backend (change port in main.py)
uvicorn.run(app, host="0.0.0.0", port=8001)

# Frontend (change port)
npm run dev -- -p 3001
```

## What's Next?

- Read [README.md](README.md) for detailed documentation
- See [DEPLOYMENT.md](DEPLOYMENT.md) for Vercel deployment
- Check API docs at http://localhost:8000/docs

## Architecture Overview

```
┌─────────────┐      HTTP       ┌──────────────┐
│   Next.js   │ ◄──────────────► │   FastAPI    │
│  (Port 3000)│                  │  (Port 8000) │
└─────────────┘                  └──────┬───────┘
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │  PostgreSQL  │
                                 │  (Port 5432) │
                                 └──────────────┘
```

## System Requirements

- **CPU:** 2+ cores recommended
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 1GB for application + storage for uploaded files
- **OS:** Windows 10+, Ubuntu 20.04+, macOS 10.15+

---

Need help? Check main README.md or open an issue on GitHub.
