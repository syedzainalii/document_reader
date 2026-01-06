# Installation Checklist ✅

Use this checklist to ensure everything is set up correctly.

## Pre-Installation

- [ ] Node.js 18+ installed (`node --version`)
- [ ] Python 3.9+ installed (`python --version`)
- [ ] PostgreSQL 12+ installed (`psql --version`)
- [ ] Tesseract OCR installed (`tesseract --version`)
- [ ] Git installed (`git --version`)

## Backend Setup

- [ ] Navigate to `server/` directory
- [ ] Create virtual environment (`python -m venv venv`)
- [ ] Activate virtual environment
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Create PostgreSQL database (`createdb university_docs`)
- [ ] Copy `.env.example` to `.env`
- [ ] Edit `.env` with your database credentials
- [ ] Update `TESSERACT_CMD` path in `.env`
- [ ] Test backend startup (`python main.py`)
- [ ] Verify API at http://localhost:8000
- [ ] Check API docs at http://localhost:8000/docs

## Frontend Setup

- [ ] Navigate to `client/` directory
- [ ] Install dependencies (`npm install`)
- [ ] Copy `.env.local.example` to `.env.local`
- [ ] Update `NEXT_PUBLIC_API_URL` in `.env.local`
- [ ] Test build (`npm run build`)
- [ ] Start development server (`npm run dev`)
- [ ] Verify frontend at http://localhost:3000

## Functionality Tests

- [ ] Dashboard loads with statistics
- [ ] Upload page accessible
- [ ] File upload works
- [ ] Camera capture works (HTTPS required)
- [ ] OCR extracts text correctly
- [ ] Student data saved to database
- [ ] Search functionality works
- [ ] Pagination works
- [ ] Student detail modal opens
- [ ] Update student works
- [ ] Delete student works
- [ ] Excel export downloads successfully
- [ ] Excel file opens with correct data

## Database Verification

```sql
-- Connect to database
psql -d university_docs

-- Check tables exist
\dt

-- Check students table structure
\d students

-- Query test data
SELECT * FROM students LIMIT 5;
```

## Common Issues Resolution

### Backend Issues

**Issue: ModuleNotFoundError**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Database connection failed**
```bash
# Solution: Check PostgreSQL is running
# Windows: services.msc → PostgreSQL
# Linux: sudo service postgresql status
# Mac: brew services list
```

**Issue: Tesseract not found**
```bash
# Windows: Install from https://github.com/UB-Mannheim/tesseract/wiki
# Update .env: TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

# Ubuntu: sudo apt-get install tesseract-ocr
# Mac: brew install tesseract
```

### Frontend Issues

**Issue: Module not found**
```bash
# Solution: Clean install
rm -rf node_modules package-lock.json
npm install
```

**Issue: Port 3000 in use**
```bash
# Solution: Use different port
npm run dev -- -p 3001
```

**Issue: API calls fail**
```bash
# Solution: Check .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000

# Verify backend is running
curl http://localhost:8000/health
```

## Performance Verification

- [ ] Dashboard loads in < 2 seconds
- [ ] Search returns results in < 1 second
- [ ] Upload processes in < 5 seconds
- [ ] Excel export completes in < 3 seconds
- [ ] Page transitions are smooth

## Security Checks

- [ ] `.env` files are in `.gitignore`
- [ ] No hardcoded credentials in code
- [ ] CORS configured correctly
- [ ] File upload size limited
- [ ] SQL injection protection (SQLAlchemy handles this)

## Deployment Readiness

### For Vercel Deployment

- [ ] Backend `vercel.json` exists
- [ ] Backend `api/index.py` exists
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Environment variables documented
- [ ] PostgreSQL database provisioned (Neon/Supabase)
- [ ] Read DEPLOYMENT.md

### Pre-Production

- [ ] All tests passing
- [ ] Error handling verified
- [ ] Loading states work
- [ ] Mobile responsive
- [ ] Documentation complete

## Success Criteria

✅ Backend API running and accessible
✅ Frontend UI responsive and functional
✅ Database connected and tables created
✅ OCR processing working
✅ File uploads successful
✅ Search and pagination working
✅ Excel export functional
✅ All pages load without errors

## Next Steps After Installation

1. **Test with real documents**
   - Upload various ID card formats
   - Verify OCR accuracy
   - Check photo extraction

2. **Customize configuration**
   - Adjust pagination size
   - Configure upload limits
   - Update CORS origins

3. **Deploy to production**
   - Follow DEPLOYMENT.md
   - Set up production database
   - Configure environment variables

4. **Monitor and optimize**
   - Check database performance
   - Monitor API response times
   - Review error logs

## Getting Help

- **Documentation**: Check README.md, QUICKSTART.md, DEPLOYMENT.md
- **API Docs**: http://localhost:8000/docs
- **Logs**: Check terminal output for errors
- **Database**: Use `psql` to inspect data

---

**Installation complete?** You should now have a fully functional University Document Management System! 🎉

Next: Upload your first student document and see the OCR magic happen!
