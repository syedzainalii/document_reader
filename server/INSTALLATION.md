# Backend Installation Guide

## Step-by-Step Installation

### 1. Create Virtual Environment

```bash
cd server
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

**Option A: Install All Dependencies (with OCR)**
```bash
pip install -r requirements.txt
```

**Option B: Install Without OCR (for testing API only)**
```bash
pip install fastapi uvicorn python-multipart sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings openpyxl numpy
```

### 4. Install Tesseract OCR (Required for OCR features)

**Windows:**
1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to default location: `C:\Program Files\Tesseract-OCR`
3. Add to PATH or update `.env` file:
   ```
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

**Verify Installation:**
```bash
tesseract --version
```

### 5. Install OpenCV (Required for photo detection)

**After activating virtual environment:**

**Windows:**
```bash
pip install opencv-python-headless
```

**Linux:**
```bash
pip install opencv-python-headless
# If you get errors, install system dependencies first:
sudo apt-get install libopencv-dev python3-opencv
```

**MacOS:**
```bash
pip install opencv-python-headless
```

### 6. Setup Database

**Create PostgreSQL Database:**
```bash
# Using createdb command
createdb university_docs

# Or using psql
psql -U postgres
CREATE DATABASE university_docs;
\q
```

### 7. Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env and update:
# - DATABASE_URL with your PostgreSQL credentials
# - TESSERACT_CMD path if on Windows
# - ALLOWED_ORIGINS with your frontend URL
```

Example `.env`:
```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/university_docs
TESSERACT_CMD=/usr/bin/tesseract
ALLOWED_ORIGINS=http://localhost:3000
UPLOAD_DIR=./uploads
DEBUG=True
```

### 8. Test the Installation

**Start the server:**
```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Database initialized successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test the API:**
- Open browser: http://localhost:8000
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Troubleshooting

### ModuleNotFoundError: No module named 'pytesseract'

**Solution:**
```bash
# Make sure virtual environment is activated
pip install pytesseract
```

### ModuleNotFoundError: No module named 'cv2'

**Solution:**
```bash
pip install opencv-python-headless
```

### Database connection error

**Solution:**
1. Verify PostgreSQL is running:
   ```bash
   # Windows
   pg_ctl status
   
   # Linux
   sudo service postgresql status
   ```

2. Test connection:
   ```bash
   psql -U postgres -d university_docs
   ```

3. Update DATABASE_URL in `.env` with correct credentials

### Tesseract not found

**Solution:**
1. Install Tesseract (see step 4)
2. Update TESSERACT_CMD in `.env`:
   ```env
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe  # Windows
   TESSERACT_CMD=/usr/bin/tesseract  # Linux/Mac
   ```

### Port 8000 already in use

**Solution:**
Edit `main.py` and change port:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## Dependencies Explained

| Package | Purpose | Required For |
|---------|---------|--------------|
| fastapi | Web framework | Core API |
| uvicorn | ASGI server | Running the app |
| python-multipart | File uploads | Document upload |
| sqlalchemy | ORM | Database |
| psycopg2-binary | PostgreSQL driver | Database |
| python-dotenv | Environment variables | Configuration |
| pydantic | Data validation | Core API |
| pytesseract | OCR | Text extraction |
| opencv-python-headless | Image processing | Photo detection |
| Pillow | Image handling | Image processing |
| openpyxl | Excel export | Data export |
| numpy | Array operations | Image processing |

## Testing Without OCR

If you want to test the API without installing OCR dependencies:

1. Install core dependencies only:
   ```bash
   pip install fastapi uvicorn python-multipart sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings openpyxl
   ```

2. Comment out OCR imports in `main.py`:
   ```python
   # from services.ocr_service import OCRService
   ```

3. Disable OCR processing in upload endpoint

## Next Steps

1. ✅ Install all dependencies
2. ✅ Setup database
3. ✅ Configure environment
4. ✅ Start server
5. ✅ Test API endpoints
6. 🚀 Start frontend (see client/README.md)

## Quick Install Script

**Windows (PowerShell):**
```powershell
cd server
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env file with your settings
python main.py
```

**Linux/Mac (Bash):**
```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env file with your settings
python main.py
```
