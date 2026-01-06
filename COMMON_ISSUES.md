# Common Issues and Solutions

Quick reference guide for resolving common issues when setting up the University Document Management System.

## 🔴 Issue: ModuleNotFoundError: No module named 'main'

**Error Message:**
```
File "D:\Web Designing\document_reader\server\api\index.py", line 5, in <module>
    from main import app
ModuleNotFoundError: No module named 'main'
```

**Why This Happens:**
- This occurs when testing the Vercel entry point (`api/index.py`) directly
- The `api/index.py` file is designed for Vercel deployment, not local testing
- Python can't find the `main` module because of import path issues

**Solution:**
Don't run `api/index.py` directly. Instead, run the main application:

```bash
cd server
python main.py
```

**For Vercel Deployment:**
The `api/index.py` file will work correctly on Vercel because it has the proper path setup in `vercel.json`.

---

## 🔴 Issue: ModuleNotFoundError: No module named 'pytesseract'

**Error Message:**
```
ModuleNotFoundError: No module named 'pytesseract'
```

**Solution:**

### Step 1: Activate Virtual Environment
```bash
cd server

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install Tesseract OCR (System Package)

**Windows:**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location
3. Add to `.env`:
   ```env
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
```

**MacOS:**
```bash
brew install tesseract
```

**Verify:**
```bash
tesseract --version
```

---

## 🔴 Issue: ModuleNotFoundError: No module named 'cv2'

**Error Message:**
```
ModuleNotFoundError: No module named 'cv2'
```

**Solution:**
```bash
cd server
venv\Scripts\activate  # or source venv/bin/activate
pip install opencv-python-headless
```

---

## 🔴 Issue: Database Connection Failed

**Error Message:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions:**

### Check 1: PostgreSQL is Running
```bash
# Windows
pg_ctl status

# Linux
sudo service postgresql status

# Mac
brew services list | grep postgresql
```

**Start PostgreSQL if stopped:**
```bash
# Windows
pg_ctl start

# Linux
sudo service postgresql start

# Mac
brew services start postgresql
```

### Check 2: Database Exists
```bash
# List databases
psql -U postgres -l

# Create if missing
createdb university_docs
```

### Check 3: Correct Connection String
Edit `server/.env`:
```env
# Format: postgresql://username:password@host:port/database
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/university_docs
```

### Check 4: Test Connection
```bash
psql -U postgres -d university_docs -c "SELECT 1;"
```

---

## 🔴 Issue: Port Already in Use

**Error Message:**
```
[ERROR] Address already in use: http://0.0.0.0:8000
```

**Solution 1: Kill Process Using Port**

**Windows:**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Find and kill
lsof -ti:8000 | xargs kill -9
```

**Solution 2: Use Different Port**

Edit `server/main.py`:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000
```

Then update `client/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

---

## 🔴 Issue: Virtual Environment Not Activating

**Windows Error:**
```
cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then retry
venv\Scripts\activate
```

---

## 🔴 Issue: CORS Errors in Browser

**Error in Browser Console:**
```
Access to fetch at 'http://localhost:8000/api/students' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:**

Edit `server/.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Restart backend server** after changing `.env` file.

---

## 🔴 Issue: OCR Returns Empty Text

**Symptoms:**
- Upload succeeds but no text is extracted
- Student data fields are empty

**Solutions:**

### Solution 1: Check Image Quality
- Use clear, high-resolution images
- Ensure good lighting
- Text should be legible
- No blur or distortion

### Solution 2: Verify Tesseract Installation
```bash
tesseract --version
```

If not found, install Tesseract OCR (see above).

### Solution 3: Check Tesseract Path
Edit `server/.env`:
```env
# Windows
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Linux/Mac
TESSERACT_CMD=/usr/bin/tesseract
```

### Solution 4: Test Tesseract Directly
```bash
tesseract your-image.jpg output.txt
cat output.txt
```

---

## 🔴 Issue: Frontend Can't Connect to Backend

**Symptoms:**
- Dashboard shows "Loading..."
- No data appears
- Console shows network errors

**Solutions:**

### Check 1: Backend is Running
```bash
# Visit in browser
http://localhost:8000

# Should show: {"message": "University Document Management System API"}
```

### Check 2: Correct API URL
Check `client/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Check 3: Restart Frontend
```bash
# Stop with Ctrl+C, then
npm run dev
```

**Note:** `.env.local` changes require frontend restart!

---

## 🔴 Issue: npm install Fails

**Error Message:**
```
npm ERR! code EINTEGRITY
```

**Solution:**
```bash
cd client

# Clear cache
rm -rf node_modules
rm package-lock.json

# Reinstall
npm cache clean --force
npm install
```

---

## 🔴 Issue: Upload Returns 500 Error

**Symptoms:**
- Upload button clicked
- Error: "Error processing upload"
- Backend shows error in logs

**Common Causes:**

### Cause 1: Missing Dependencies
```bash
cd server
pip install pillow opencv-python-headless pytesseract
```

### Cause 2: Tesseract Not Found
Install Tesseract OCR (see above) and configure path in `.env`.

### Cause 3: Upload Directory Permissions
```bash
cd server
mkdir uploads
chmod 755 uploads  # Linux/Mac
```

### Cause 4: File Too Large
Edit `server/.env`:
```env
MAX_FILE_SIZE=20971520  # 20MB instead of default 10MB
```

---

## 🔴 Issue: Photo Not Extracted

**Symptoms:**
- Text is extracted successfully
- But "Student photo extracted" doesn't appear
- No photo in student details

**Solutions:**

### Solution 1: Verify OpenCV Installation
```bash
pip show opencv-python-headless
# Should show version info
```

If not installed:
```bash
pip install opencv-python-headless
```

### Solution 2: Use Clear Face Photo
- Photo should show face clearly
- Front-facing photo works best
- Adequate lighting
- No heavy shadows or obstructions

### Solution 3: Check Logs
Look at backend terminal for error messages during upload.

---

## 🔴 Issue: Excel Export Doesn't Work

**Symptoms:**
- Click "Export to Excel" button
- Nothing happens or error appears

**Solutions:**

### Solution 1: Install openpyxl
```bash
cd server
pip install openpyxl
```

### Solution 2: Check Backend Logs
Look for export-related errors in backend terminal.

### Solution 3: Test API Directly
Visit in browser:
```
http://localhost:8000/api/export/excel
```

Should download an Excel file.

---

## 📋 Quick Diagnostic Commands

### Check All Prerequisites
```bash
# Python version
python --version

# Node version
node --version

# PostgreSQL version
psql --version

# Tesseract version
tesseract --version

# Check if backend is running
curl http://localhost:8000/health

# Check if frontend is running
curl http://localhost:3000
```

### View Logs
```bash
# Backend logs - check terminal where you ran: python main.py
# Frontend logs - check terminal where you ran: npm run dev
# Browser logs - Press F12 → Console tab
```

### Environment Variables
```bash
# Backend
cd server
cat .env

# Frontend
cd client
cat .env.local
```

---

## 🆘 Still Having Issues?

### Automated Setup
Try the automated setup scripts:

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

### Clean Installation

**Backend:**
```bash
cd server
rm -rf venv
rm -rf __pycache__
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd client
rm -rf node_modules .next
npm install
npm run dev
```

### Check Documentation
1. `QUICKSTART.md` - 5-minute setup guide
2. `INSTALLATION_CHECKLIST.md` - Complete checklist
3. `server/INSTALLATION.md` - Detailed backend setup
4. `README.md` - Full documentation

### System Requirements
- Windows 10+, Ubuntu 20.04+, or macOS 10.15+
- 4GB RAM minimum (8GB recommended)
- 1GB disk space
- Internet connection for dependencies

---

## 📞 Getting Help

If you're still stuck:

1. Check error messages carefully
2. Search the error message online
3. Review documentation files
4. Check that all prerequisites are installed
5. Try clean installation (see above)

**Common mistake:** Forgetting to activate virtual environment before installing packages or running the app!

**Remember:** Always activate the virtual environment:
```bash
# Backend
cd server
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Then run commands
python main.py
```
