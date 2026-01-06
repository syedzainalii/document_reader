# Quick Start - NED University Backend

## ⚡ Super Fast Start (Windows)

Double-click: **`START_SERVER.bat`**

That's it! The script will:
1. Activate virtual environment
2. Check if packages are installed
3. Install missing packages if needed
4. Check for .env file
5. Start the server

---

## 📋 Manual Start (All Platforms)

### Windows

```bash
cd D:\Web Designing\document_reader\server
venv\Scripts\activate
python main.py
```

### Linux/Mac

```bash
cd /path/to/document_reader/server
source venv/bin/activate
python main.py
```

---

## ❌ Common Mistakes

### WRONG: Running api/index.py
```bash
cd api
python index.py  ❌ DON'T DO THIS
```

**Why wrong?** `api/index.py` is only for Vercel deployment!

### RIGHT: Running main.py
```bash
cd server
venv\Scripts\activate
python main.py  ✅ DO THIS
```

---

## 🔧 First Time Setup

If this is your first time:

### 1. Create Virtual Environment (if not exists)
```bash
cd server
python -m venv venv
```

### 2. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env File
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and set:
- Database connection
- Admin credentials
- JWT secret key

### 5. Create Database
```bash
createdb ned_university_docs
```

### 6. Start Server
```bash
python main.py
```

---

## ✅ Verify It's Working

1. Server starts with message:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   Database initialized successfully
   ```

2. Open browser: http://localhost:8000
   - Should show: `{"message": "NED University Document Management System API"...}`

3. Check API docs: http://localhost:8000/docs
   - Should show interactive API documentation

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### "Database connection failed"

**Solution:**
1. Start PostgreSQL service
2. Check DATABASE_URL in .env
3. Create database: `createdb ned_university_docs`

### "Port 8000 already in use"

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### Server starts but frontend can't connect

**Check:**
1. Backend running on http://localhost:8000
2. Frontend .env.local has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. CORS settings in backend .env: `ALLOWED_ORIGINS=http://localhost:3000`

---

## 📁 File Structure

```
server/
├── main.py              ← RUN THIS! ✅
├── api/
│   └── index.py         ← DON'T RUN THIS! ❌ (Vercel only)
├── venv/                ← Virtual environment
├── .env                 ← Configuration
└── START_SERVER.bat     ← Quick start script
```

---

## 🚀 Development Workflow

**Terminal 1 - Backend:**
```bash
cd server
venv\Scripts\activate
python main.py
```
Keep this running!

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```
Keep this running!

**Browser:**
http://localhost:3000

---

## 📝 Key Points

1. ✅ Always run `python main.py` from the `server` folder
2. ✅ Always activate virtual environment first
3. ❌ Never run `api/index.py` directly (it's for Vercel)
4. ✅ Use `START_SERVER.bat` for quick starts on Windows

---

## 🎯 Ready Checklist

Before starting server, verify:

- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] Dependencies installed (`pip list | grep fastapi`)
- [ ] `.env` file exists and configured
- [ ] PostgreSQL is running
- [ ] Database created (`ned_university_docs`)
- [ ] Not in `api` folder (should be in `server` folder)

---

**Need more help? Check:**
- `NED_UNIVERSITY_SETUP.md` - Complete setup guide
- `INSTALLATION_FIX.md` - Installation troubleshooting
- `COMMON_ISSUES.md` - Common problems and solutions
