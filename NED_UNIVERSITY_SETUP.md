# NED University Document Management System - Setup Guide

## 🎓 Overview

This is a **secure, modern document management system** specifically designed for **NED University of Engineering & Technology**. The system features:

- 🔐 **Admin-only access** with JWT authentication
- 🎨 **Modern UI** with emerald/teal theme (NED colors)
- ⚡ **Fast performance** optimized for 5000+ students
- 📸 **OCR & photo extraction** from student documents
- 📊 **Excel export** functionality
- 🔒 **Secure database** with PostgreSQL

---

## 🚀 Quick Start

### 1. Create Database

```bash
# Create NED University database
createdb ned_university_docs
```

### 2. Start Backend

```bash
cd server

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install authentication dependencies
pip install python-jose[cryptography] passlib[bcrypt]

# Start server
python main.py
```

### 3. Start Frontend

```bash
cd client
npm run dev
```

### 4. Login

Open http://localhost:3000 and you'll be redirected to the login page.

**Default Admin Credentials:**
- Username: `admin`
- Password: `ned@admin123`

---

## 🔐 Authentication System

### How It Works

1. **Login Page** (`/login`) - Beautiful emerald-themed login
2. **JWT Token** - Stored in localStorage, expires in 8 hours
3. **Protected Routes** - All routes require authentication except login
4. **Logout Button** - Red logout button in navbar

### Security Features

- ✅ JWT token-based authentication
- ✅ Token expiration (8 hours default)
- ✅ Automatic redirect to login if unauthorized
- ✅ All API endpoints protected with `require_admin` dependency
- ✅ Password-protected admin access

### Changing Admin Credentials

Edit `server/.env`:

```env
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_password
JWT_SECRET_KEY=your-very-secret-key-change-this
```

**Important:** Change `JWT_SECRET_KEY` in production!

---

## 🎨 Modern UI Design

### Color Scheme

- **Primary:** Emerald (Green) - `from-emerald-500 to-teal-600`
- **Accent:** Teal/Cyan
- **Background:** Gradient `from-gray-50 to-gray-100`

### Design Features

- ✨ Glassmorphism effects
- 🎭 Smooth transitions and animations
- 📱 Fully responsive (mobile-friendly)
- 🔄 Loading states with modern spinners
- 🎯 Hover effects on all interactive elements
- 🌈 Gradient backgrounds and cards

### Performance Optimizations

- ⚡ Fast page loads
- 🔄 Optimized re-renders
- 📦 Lazy loading where needed
- 🎯 Efficient API calls with auth headers

---

## 📋 Features

### Dashboard (`/`)
- Welcome banner with NED branding
- Quick action cards (Upload, Students, Export)
- Statistics with animated progress bars
- Department breakdown
- Modern feature showcase

### Login Page (`/login`)
- Beautiful emerald gradient design
- Secure JWT authentication
- Error handling with user-friendly messages
- Default credentials display (for demo)
- NED University branding

### Upload Page (`/upload`)
- File upload with drag & drop
- Camera capture for live photos
- OCR processing with results display
- Modern UI with icons

### Students Page (`/students`)
- Search functionality
- Pagination
- Student detail modal
- Delete functionality
- Excel export

---

## 🔧 Technical Details

### Backend Changes

1. **Authentication Module** (`auth.py`)
   - JWT token creation and verification
   - Password hashing (bcrypt)
   - Admin authentication

2. **Auth Schemas** (`schemas_auth.py`)
   - LoginRequest
   - TokenResponse
   - UserResponse

3. **Protected Endpoints**
   - All `/api/` routes require authentication
   - `require_admin` dependency added to all endpoints

4. **New Endpoints**
   - `POST /api/auth/login` - Admin login
   - `GET /api/auth/me` - Get current user info

### Frontend Changes

1. **Auth Service** (`lib/auth.ts`)
   - Login/logout functionality
   - Token management
   - localStorage handling

2. **Auth Guard** (`components/AuthGuard.tsx`)
   - Route protection
   - Automatic redirect to login
   - Loading state during auth check

3. **Login Page** (`app/login/page.tsx`)
   - Modern login UI
   - Form validation
   - Error handling

4. **Updated Layout** (`app/layout.tsx`)
   - AuthGuard wrapper
   - Logout button in navbar
   - NED branding
   - Modern emerald theme

5. **API Client** (`lib/api.ts`)
   - Auth headers added to all requests
   - Token automatically included

---

## 🎯 Usage Guide

### For Administrators

1. **Login**
   - Visit http://localhost:3000
   - Enter admin credentials
   - You'll be redirected to dashboard

2. **Upload Documents**
   - Click "Upload Documents" card
   - Choose file or use camera
   - System extracts data automatically
   - Review extracted information

3. **Manage Students**
   - Click "View Students" card
   - Search by ID or name
   - Click student to view details
   - Delete if needed

4. **Export Data**
   - Click "Export to Excel" on dashboard or students page
   - Excel file downloads automatically

5. **Logout**
   - Click red "Logout" button in navbar
   - Redirected to login page
   - Token cleared from browser

---

## 🔒 Security Best Practices

### For Production Deployment

1. **Change Default Credentials**
   ```env
   ADMIN_USERNAME=secure_admin
   ADMIN_PASSWORD=VerySecurePassword123!
   ```

2. **Generate Strong JWT Secret**
   ```bash
   # Generate random secret
   openssl rand -hex 32
   ```
   
   Add to `.env`:
   ```env
   JWT_SECRET_KEY=<generated-secret-key>
   ```

3. **Use HTTPS**
   - Deploy with SSL certificate
   - Enable secure cookies

4. **Set Proper Token Expiration**
   ```env
   ACCESS_TOKEN_EXPIRE_MINUTES=480  # 8 hours (adjust as needed)
   ```

5. **Database Security**
   - Use strong PostgreSQL password
   - Restrict database access
   - Enable SSL connection

6. **CORS Configuration**
   ```env
   ALLOWED_ORIGINS=https://your-frontend-domain.com
   ```

---

## 📊 Database

### Connection

Update `server/.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/ned_university_docs
```

### Tables

- **students** - Student records with OCR data

The database is automatically created when you start the backend.

---

## 🚀 Deployment

### Backend (Vercel)

```bash
cd server
vercel
```

**Environment Variables:**
- `DATABASE_URL`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `JWT_SECRET_KEY`
- `ALLOWED_ORIGINS`

### Frontend (Vercel)

```bash
cd client
vercel
```

**Environment Variables:**
- `NEXT_PUBLIC_API_URL` - Your backend URL

---

## 🎨 Customization

### Change Theme Colors

Edit Tailwind classes in components:

**Current:** `from-emerald-500 to-teal-600`
**Options:**
- Blue: `from-blue-500 to-indigo-600`
- Purple: `from-purple-500 to-pink-600`
- Orange: `from-orange-500 to-red-600`

### Add More Admins

Currently supports single admin. To add multiple admins:

1. Create `admins` table in database
2. Update `authenticate_admin()` in `auth.py` to query database
3. Create admin management UI

---

## 📝 Default Credentials

**⚠️ IMPORTANT:** Change these in production!

- **Username:** `admin`
- **Password:** `ned@admin123`
- **Token Expiry:** 8 hours

---

## 🐛 Troubleshooting

### "Incorrect username or password"

- Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `server/.env`
- Restart backend after changing credentials

### "Failed to fetch" on Dashboard

- Backend not running - start with `python main.py`
- Check `NEXT_PUBLIC_API_URL` in `client/.env.local`

### "Unauthorized" errors

- Token expired - login again
- Clear browser localStorage and login again
- Check JWT_SECRET_KEY matches between requests

### Login page shows but can't login

- Backend not running
- Check backend logs for errors
- Verify database connection

---

## 📚 File Structure

```
server/
├── auth.py               # Authentication logic (NEW)
├── schemas_auth.py       # Auth schemas (NEW)
├── main.py              # Updated with auth
├── config.py            # Updated with auth settings
└── .env                 # Auth credentials

client/
├── app/
│   ├── login/
│   │   └── page.tsx     # Login page (NEW)
│   ├── layout.tsx       # Updated with AuthGuard
│   └── page.tsx         # Updated dashboard design
├── components/
│   └── AuthGuard.tsx    # Route protection (NEW)
├── lib/
│   ├── auth.ts          # Auth service (NEW)
│   └── api.ts           # Updated with auth headers
└── middleware.ts        # Auth middleware (NEW)
```

---

## ✨ What's New

### Backend
✅ JWT authentication system
✅ Login endpoint
✅ Protected API routes
✅ Admin-only access
✅ Token validation
✅ NED branding

### Frontend
✅ Beautiful login page
✅ AuthGuard component
✅ Automatic auth redirect
✅ Logout functionality
✅ Modern emerald/teal theme
✅ Smooth animations
✅ NED University branding
✅ Performance optimizations

---

## 📞 Support

For NED University staff:
- Check logs in backend terminal
- See COMMON_ISSUES.md for troubleshooting
- Contact IT department for database access

---

**Built with ❤️ for NED University of Engineering & Technology**
