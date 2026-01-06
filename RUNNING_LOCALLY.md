# Running the Application Locally

## Prerequisites

1. **PostgreSQL** installed and running
2. **Python 3.11+** installed
3. **Node.js 18+** installed

## First-Time Setup

### 1. Setup Database (Required - First Time Only)

Run the database setup script:

```bash
# Windows
cd server
SETUP_DATABASE.bat

# Mac/Linux
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup_database.py
```

This will:
- Create the `ned_university_docs` database
- Initialize all required tables
- Verify the setup

**If you prefer manual setup:**
```sql
# Open PostgreSQL command line (psql)
psql -U postgres

# Create the database
CREATE DATABASE ned_university_docs;

# Exit psql
\q
```

## Quick Start

### Option 1: Use the Start Script (Windows)

Simply double-click or run:
```bash
START_SERVERS.bat
```

This will automatically:
- Create Python virtual environment if needed
- Install backend dependencies
- Start backend server on http://localhost:8000
- Start frontend server on http://localhost:3000

### Option 2: Manual Start

#### 1. Start Backend Server

```bash
# Navigate to server directory
cd server

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the server
python main.py
```

Backend will be available at: http://localhost:8000

#### 2. Start Frontend Server

Open a new terminal:

```bash
# Navigate to client directory
cd client

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## Verifying the Servers

### Check Backend
Open http://localhost:8000 in your browser or run:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status": "healthy", "timestamp": "..."}
```

### Check Frontend
Open http://localhost:3000 in your browser

## Troubleshooting

### "Failed to fetch" Error

**Problem**: Frontend shows "Failed to fetch" error in console

**Solution**: Make sure the backend server is running on port 8000

1. Check if backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. If not running, start it:
   ```bash
   cd server
   venv\Scripts\activate
   python main.py
   ```

### Port Already in Use

**Backend (Port 8000)**:
```bash
# Windows - Find and kill process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (Port 3000)**:
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <process_id> /F

# Mac/Linux
lsof -ti:3000 | xargs kill -9
```

### Database Connection Error

**Error**: `database "ned_university_docs" does not exist`

**Solution**: Run the database setup script:

```bash
cd server
# Windows:
SETUP_DATABASE.bat

# Mac/Linux:
python setup_database.py
```

**Or create manually**:
```bash
# Check if PostgreSQL is running
# Windows: Services -> PostgreSQL
# Mac: brew services list
# Linux: sudo systemctl status postgresql

# Create database
psql -U postgres
CREATE DATABASE ned_university_docs;
\q
```

### Python Dependencies Error

```bash
cd server
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Node Modules Error

```bash
cd client
rm -rf node_modules package-lock.json
npm install
```

## Environment Variables

### Backend (.env in server/)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ned_university_docs
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
JWT_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend (.env.local in client/)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Default Login Credentials

- **Username**: `admin`
- **Password**: `admin`

⚠️ **Important**: Change these in production!

## Development Tips

### Hot Reload

Both servers support hot reload:
- **Backend**: Automatically reloads when Python files change
- **Frontend**: Automatically reloads when React/Next.js files change

### Checking Logs

**Backend**: Logs appear in the terminal where you ran `python main.py`

**Frontend**: 
- Server logs: Terminal where you ran `npm run dev`
- Browser logs: Open DevTools (F12) → Console tab

### API Documentation

Once the backend is running, visit:
- API Docs (Swagger): http://localhost:8000/docs
- Alternative Docs (ReDoc): http://localhost:8000/redoc

## Need Help?

1. Check `TROUBLESHOOTING_FETCH_ERROR.md` for API connection issues
2. Check `server/README.md` for backend-specific help
3. Check `client/README.md` for frontend-specific help
4. Check GitHub issues: https://github.com/syedzainalii/document_reader/issues
