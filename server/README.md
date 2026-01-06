# Backend API - University Document Management System

FastAPI backend with OCR processing, PostgreSQL database, and Vercel deployment support.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run server
python main.py
```

Server runs at: http://localhost:8000
API docs: http://localhost:8000/docs

## API Documentation

### Upload Document
```http
POST /api/upload
Content-Type: multipart/form-data

file: [binary]
```

**Response:**
```json
{
  "success": true,
  "message": "Document uploaded and processed successfully",
  "student": {
    "id": 1,
    "student_id": "CS20221234",
    "full_name": "John Doe",
    "email": "john@university.edu",
    ...
  },
  "ocr_result": {
    "success": true,
    "extracted_text": "...",
    "photo_extracted": true
  }
}
```

### Search Students
```http
GET /api/students?query=john&page=1&page_size=50
```

**Response:**
```json
{
  "total": 100,
  "page": 1,
  "page_size": 50,
  "students": [...]
}
```

### Export to Excel
```http
GET /api/export/excel?query=CS2022
```

Returns Excel file download.

## Database Schema

### Students Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| student_id | VARCHAR(50) | Unique student ID |
| full_name | VARCHAR(200) | Student name |
| email | VARCHAR(200) | Email address |
| phone | VARCHAR(50) | Phone number |
| department | VARCHAR(200) | Department |
| program | VARCHAR(200) | Program/course |
| year_of_study | VARCHAR(50) | Year level |
| document_type | VARCHAR(100) | Document type |
| extracted_text | TEXT | Raw OCR text |
| original_image_path | VARCHAR(500) | Document path |
| photo_path | VARCHAR(500) | Student photo path |
| created_at | TIMESTAMP | Creation time |
| updated_at | TIMESTAMP | Update time |

## Vercel Deployment

### Configuration

The `vercel.json` file configures serverless deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### Environment Variables

Set in Vercel dashboard:
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_ORIGINS` - Frontend URL
- `UPLOAD_DIR` - Use `/tmp/uploads` for Vercel

### Limitations

- File storage is ephemeral on Vercel (use cloud storage for production)
- Tesseract OCR may not work on serverless (consider external OCR API)
- Cold starts may occur

## Development

### Project Structure

```
server/
├── api/
│   └── index.py          # Vercel entry point
├── services/
│   ├── ocr_service.py    # OCR processing
│   └── excel_service.py  # Excel export
├── config.py             # Settings
├── database.py           # DB connection
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic schemas
├── main.py               # FastAPI app
└── requirements.txt      # Dependencies
```

### Adding New Endpoints

1. Add route in `main.py`:
```python
@app.get("/api/new-endpoint")
async def new_endpoint(db: Session = Depends(get_db)):
    return {"message": "Hello"}
```

2. Test locally
3. Deploy to Vercel

### Database Migrations

For schema changes, use Alembic:

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init migrations

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

## Testing

```bash
# Install test dependencies
pip install pytest httpx

# Run tests
pytest

# With coverage
pytest --cov=.
```

## Performance Tips

- Use database indexes (already configured)
- Enable connection pooling
- Cache frequent queries
- Optimize OCR preprocessing
- Use async endpoints for I/O operations

## Security

- Validate file uploads
- Sanitize OCR text
- Use parameterized queries (SQLAlchemy handles this)
- Add rate limiting
- Implement authentication
- Enable CORS only for trusted origins

## Troubleshooting

**Database connection fails:**
- Check DATABASE_URL format
- Verify PostgreSQL is running
- Test connection: `psql $DATABASE_URL`

**OCR returns empty text:**
- Check image quality
- Verify Tesseract installation
- Try preprocessing adjustments

**Import errors:**
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
