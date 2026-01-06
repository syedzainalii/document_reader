# University Document Management System

A complete full-stack system for managing university student documents with automated OCR text extraction and photo detection.

## 🚀 Features

- **Document Upload**: Upload student ID cards and forms via file upload or camera capture
- **OCR Text Extraction**: Automatically extract student information from documents using Tesseract
- **Photo Detection**: Detect and extract student photos from documents using OpenCV
- **Database Storage**: Store all student data in PostgreSQL with efficient indexing
- **Smart Search**: Search students by ID or name with pagination (handles 5000+ students)
- **Excel Export**: Export all student data to formatted Excel spreadsheets
- **Responsive UI**: Modern, mobile-friendly interface built with Next.js and Tailwind CSS
- **Vercel Ready**: Both frontend and backend configured for Vercel deployment

## 🛠️ Tech Stack

### Frontend
- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **React Hooks** for state management

### Backend
- **FastAPI** (Python) for REST API
- **SQLAlchemy** for ORM
- **PostgreSQL** for database
- **Tesseract OCR** for text extraction
- **OpenCV** for image processing
- **Pillow** for image handling
- **openpyxl** for Excel export

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.9+
- **PostgreSQL** 12+
- **Tesseract OCR** installed on system

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd document_reader
```

### 2. Backend Setup

```bash
cd server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Ubuntu: sudo apt-get install tesseract-ocr
# Mac: brew install tesseract

# Create .env file
copy .env.example .env

# Edit .env and configure:
# - DATABASE_URL (PostgreSQL connection string)
# - TESSERACT_CMD (path to tesseract executable)
# - ALLOWED_ORIGINS (add your frontend URL)
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb university_docs

# Or using psql:
psql -U postgres
CREATE DATABASE university_docs;
\q

# The application will automatically create tables on startup
```

### 4. Frontend Setup

```bash
cd ../client

# Install dependencies
npm install

# Create .env.local file
copy .env.local.example .env.local

# Edit .env.local and set:
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd server
venv\Scripts\activate  # or source venv/bin/activate
python main.py
# Backend runs at http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
# Frontend runs at http://localhost:3000
```

Open http://localhost:3000 in your browser.

## 📦 Deployment to Vercel

### Backend Deployment

1. **Prepare PostgreSQL Database**
   - Use managed PostgreSQL (Neon, Supabase, Railway, etc.)
   - Get connection string

2. **Deploy to Vercel**
   ```bash
   cd server
   vercel
   ```

3. **Configure Environment Variables in Vercel Dashboard:**
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `ALLOWED_ORIGINS`: Your frontend URL
   - `UPLOAD_DIR`: `/tmp/uploads` (Vercel uses /tmp for serverless)

4. **Note**: Tesseract OCR may have limitations on Vercel serverless. Consider:
   - Using external OCR API (Google Vision, AWS Textract)
   - Or deploying backend to Railway/Render with full system access

### Frontend Deployment

1. **Deploy to Vercel**
   ```bash
   cd client
   vercel
   ```

2. **Configure Environment Variables:**
   - `NEXT_PUBLIC_API_URL`: Your backend API URL

3. **Done!** Your frontend will be live at your Vercel URL

## 📁 Project Structure

```
document_reader/
├── server/                  # FastAPI Backend
│   ├── api/
│   │   └── index.py        # Vercel entry point
│   ├── services/
│   │   ├── ocr_service.py  # OCR processing
│   │   └── excel_service.py # Excel export
│   ├── config.py           # Configuration
│   ├── database.py         # Database setup
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── main.py             # FastAPI app
│   ├── requirements.txt    # Python dependencies
│   └── vercel.json         # Vercel config
│
├── client/                  # Next.js Frontend
│   ├── app/
│   │   ├── page.tsx        # Dashboard
│   │   ├── upload/
│   │   │   └── page.tsx    # Upload page
│   │   ├── students/
│   │   │   └── page.tsx    # Students list
│   │   └── layout.tsx      # Root layout
│   ├── lib/
│   │   └── api.ts          # API client
│   ├── next.config.ts      # Next.js config
│   └── package.json
│
└── README.md
```

## 🎯 API Endpoints

### Upload & Processing
- `POST /api/upload` - Upload document with OCR processing

### Student Management
- `GET /api/students` - Search/list students (paginated)
- `GET /api/students/{id}` - Get student details
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Data Export
- `GET /api/export/excel` - Export to Excel

### Utility
- `GET /api/stats` - Get system statistics
- `GET /api/files/{student_id}/{filename}` - Serve student files
- `GET /health` - Health check

## 🔍 Usage Guide

### 1. Upload Document

**Method 1: File Upload**
- Navigate to Upload page
- Click "Choose File"
- Select student document (ID card, form)
- Click "Upload & Process"

**Method 2: Camera Capture**
- Navigate to Upload page
- Click "Use Camera"
- Position document in frame
- Click "Capture Photo"
- Click "Upload & Process"

### 2. View Students
- Navigate to Students page
- Search by student ID or name
- Click on any student to view details
- Delete records if needed

### 3. Export Data
- Click "Export to Excel" button
- Excel file will download automatically
- Opens in Excel/LibreOffice/Google Sheets

## 🧪 Testing

### Backend Tests
```bash
cd server
pytest
```

### Frontend Tests
```bash
cd client
npm test
```

## ⚙️ Configuration

### Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/university_docs
APP_NAME="University Document Management System"
DEBUG=True
UPLOAD_DIR=./uploads
ALLOWED_ORIGINS=http://localhost:3000
TESSERACT_CMD=/usr/bin/tesseract
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=University Document Management System
```

## 🐛 Troubleshooting

### OCR Not Working
- Verify Tesseract is installed: `tesseract --version`
- Check TESSERACT_CMD path in .env
- Ensure image quality is good (clear text, good lighting)

### Database Connection Failed
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists: `psql -l`

### Camera Not Working
- Check browser permissions
- Use HTTPS (required for camera access)
- Try different browser

### Vercel Deployment Issues
- Check build logs in Vercel dashboard
- Verify environment variables are set
- For OCR issues on Vercel, consider external OCR service

## 📊 Performance

- **Database**: Indexed queries handle 5000+ students efficiently
- **Pagination**: 50 students per page by default
- **Upload Size**: Max 10MB per file (configurable)
- **Concurrent Users**: FastAPI handles async requests efficiently

## 🔒 Security Considerations

- Add authentication (JWT, OAuth)
- Implement file upload validation
- Add rate limiting
- Use HTTPS in production
- Sanitize OCR output
- Add CSRF protection

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📄 License

MIT License - feel free to use for any purpose

## 👥 Support

For issues and questions:
- Open GitHub issue
- Check documentation
- Review troubleshooting section

## 🎓 Future Enhancements

- [ ] Multi-language OCR support
- [ ] Batch document upload
- [ ] Advanced search filters
- [ ] Document version history
- [ ] Email notifications
- [ ] REST API documentation (Swagger)
- [ ] Mobile app (React Native)
- [ ] Document templates
- [ ] Data analytics dashboard
- [ ] Cloud storage integration (S3, Azure Blob)

---

Built with ❤️ for university document management
