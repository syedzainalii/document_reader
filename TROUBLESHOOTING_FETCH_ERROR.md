# Troubleshooting "Failed to Fetch" Error

## Error: TypeError: Failed to fetch

This error occurs when the frontend (Next.js) cannot connect to the backend (FastAPI) API.

## Quick Diagnosis Checklist

### 1. Is the Backend Running? ⭐ MOST COMMON ISSUE

**Check if backend is running:**
```bash
# Open browser and visit:
http://localhost:8000

# Or use curl:
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy", "timestamp": "..."}
```

**If you get an error:**
→ The backend is NOT running! Start it:

```bash
cd server
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

python main.py
```

### 2. Check Environment Variables

**Check `client/.env.local` file exists:**
```bash
# Windows
type client\.env.local

# Linux/Mac
cat client/.env.local
```

**Should contain:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**If file doesn't exist:**
```bash
cd client
copy .env.local.example .env.local  # Windows
# or
cp .env.local.example .env.local    # Linux/Mac
```

**After creating/editing `.env.local`:**
- **MUST RESTART** the frontend server
- Press `Ctrl+C` in frontend terminal
- Run `npm run dev` again

### 3. Check Port Numbers

**Backend should be on port 8000:**
- Visit: http://localhost:8000
- If using different port, update `.env.local`

**Frontend should be on port 3000:**
- Visit: http://localhost:3000
- Check terminal for actual port

### 4. Check Browser Console

**Open Browser DevTools:**
- Press F12
- Go to Console tab
- Look for the actual error

**Common errors:**

**"net::ERR_CONNECTION_REFUSED"**
→ Backend is not running

**"CORS policy"**
→ Backend CORS settings issue (see solution below)

**"404 Not Found"**
→ API endpoint issue (check backend routes)

## Step-by-Step Fix

### Step 1: Start Backend (if not running)

**Open Terminal 1:**
```bash
cd server
venv\Scripts\activate  # Windows: venv\Scripts\activate
python main.py
```

**Wait for:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
Database initialized successfully
INFO:     Application startup complete.
```

### Step 2: Verify Backend is Accessible

**Open browser:**
```
http://localhost:8000
```

**Should see:**
```json
{
  "message": "University Document Management System API",
  "version": "1.0.0",
  "status": "running"
}
```

### Step 3: Check/Create `.env.local`

**In `client/.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=University Document Management System
```

### Step 4: Restart Frontend

**Terminal 2:**
```bash
# Stop with Ctrl+C
# Then restart:
cd client
npm run dev
```

**Important:** Environment variable changes require restart!

### Step 5: Test Connection

**Open browser:**
```
http://localhost:3000
```

Dashboard should load with data.

## Common Scenarios

### Scenario 1: Backend Not Running

**Symptoms:**
- "Failed to fetch" error
- Dashboard shows "Loading..." forever
- Browser console: "ERR_CONNECTION_REFUSED"

**Solution:**
```bash
cd server
venv\Scripts\activate
python main.py
```

### Scenario 2: Wrong API URL

**Symptoms:**
- Backend is running but frontend can't connect
- Console shows 404 errors

**Solution:**
Edit `client/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Then restart frontend:**
```bash
cd client
# Ctrl+C to stop
npm run dev
```

### Scenario 3: CORS Error

**Symptoms:**
- Backend running
- Console error: "blocked by CORS policy"

**Solution:**
Edit `server/.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Then restart backend:**
```bash
cd server
python main.py
```

### Scenario 4: Port Conflicts

**Backend port 8000 in use:**
```bash
# Change port in server/main.py
uvicorn.run(app, host="0.0.0.0", port=8001)

# Update client/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8001

# Restart both servers
```

**Frontend port 3000 in use:**
```bash
# Use different port
npm run dev -- -p 3001
```

## Verification Commands

### Check if Ports are Open

**Windows:**
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

**Linux/Mac:**
```bash
lsof -i :8000
lsof -i :3000
```

### Test API Directly

**Using curl:**
```bash
# Health check
curl http://localhost:8000/health

# Get students
curl http://localhost:8000/api/students

# Get stats
curl http://localhost:8000/api/stats
```

**Using browser:**
```
http://localhost:8000/docs
```
This opens the interactive API documentation.

## Still Not Working?

### 1. Check Firewall

**Windows Firewall may block connections:**
- Open Windows Defender Firewall
- Allow Python through firewall
- Allow Node.js through firewall

### 2. Check Antivirus

Some antivirus software blocks local connections:
- Temporarily disable and test
- Add exception for Python and Node.js

### 3. Use 127.0.0.1 Instead of localhost

**Edit `client/.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 4. Check Network Settings

**Disable VPN** if using one - it may interfere with local connections.

### 5. Clear Browser Cache

- Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
- Or clear browser cache completely

## Complete Reset (Nuclear Option)

If nothing works, try a complete reset:

### Backend:
```bash
cd server

# Stop server (Ctrl+C)

# Deactivate venv
deactivate

# Delete and recreate
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Restart
python main.py
```

### Frontend:
```bash
cd client

# Stop server (Ctrl+C)

# Delete and recreate
rm -rf node_modules .next
npm install

# Restart
npm run dev
```

## How to Prevent This Error

### Every Time You Start Working:

**Terminal 1 - Backend:**
```bash
cd server
venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

**Keep both terminals open!**

### Checklist Before Starting:
- [ ] PostgreSQL is running
- [ ] Backend virtual environment activated
- [ ] Backend `.env` file configured
- [ ] Frontend `.env.local` file configured
- [ ] Both servers running (check terminals)
- [ ] Can access http://localhost:8000
- [ ] Can access http://localhost:3000

## Quick Reference

| Issue | Check This | Fix This |
|-------|------------|----------|
| Failed to fetch | Backend running? | Start backend: `python main.py` |
| Connection refused | Port 8000 open? | Check if backend is listening |
| CORS error | ALLOWED_ORIGINS? | Update `server/.env` |
| 404 errors | API URL correct? | Check `client/.env.local` |
| Still loading | Restart frontend? | Restart after `.env.local` changes |

---

**Most Common Fix:**
```bash
# Terminal 1
cd server
venv\Scripts\activate
python main.py

# Terminal 2  
cd client
npm run dev

# Both should stay running!
```

**Remember:** Both backend AND frontend must be running simultaneously!
