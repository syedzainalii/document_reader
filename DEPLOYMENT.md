# Deployment Guide - University Document Management System

Complete guide for deploying both frontend and backend to Vercel.

## Prerequisites

- Vercel account (https://vercel.com)
- PostgreSQL database (Neon, Supabase, or Railway)
- GitHub repository (optional but recommended)

## Backend Deployment to Vercel

### Step 1: Prepare Database

1. **Create PostgreSQL Database**
   
   **Option A: Neon (Recommended)**
   - Visit https://neon.tech
   - Create free account
   - Create new project
   - Copy connection string

   **Option B: Supabase**
   - Visit https://supabase.com
   - Create project
   - Go to Settings → Database
   - Copy connection string

   **Option C: Railway**
   - Visit https://railway.app
   - Create PostgreSQL database
   - Copy connection string

2. **Connection String Format:**
   ```
   postgresql://user:password@host:5432/database?sslmode=require
   ```

### Step 2: Deploy Backend

```bash
cd server

# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

Follow prompts:
- Set project name
- Select scope
- Link to existing project or create new

### Step 3: Configure Environment Variables

In Vercel Dashboard (https://vercel.com/dashboard):

1. Go to your project → Settings → Environment Variables
2. Add the following:

```
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
ALLOWED_ORIGINS=https://your-frontend.vercel.app
UPLOAD_DIR=/tmp/uploads
DEBUG=False
```

### Step 4: Redeploy

```bash
vercel --prod
```

Your backend is now live! Note the URL (e.g., `https://your-backend.vercel.app`)

## Frontend Deployment to Vercel

### Step 1: Deploy Frontend

```bash
cd client

# Install Vercel CLI (if not already installed)
npm install -g vercel

# Deploy
vercel
```

### Step 2: Configure Environment Variables

In Vercel Dashboard:

1. Go to your frontend project → Settings → Environment Variables
2. Add:

```
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

### Step 3: Redeploy

```bash
vercel --prod
```

Your frontend is now live!

## Post-Deployment

### 1. Update CORS

Go back to backend environment variables and update:
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://*.vercel.app
```

### 2. Test the System

Visit your frontend URL and test:
- [ ] Dashboard loads with statistics
- [ ] Upload document works
- [ ] OCR extraction works
- [ ] Search students works
- [ ] Excel export works

## Important Notes

### File Storage Limitations

Vercel serverless functions have ephemeral file storage. For production:

1. **Use Cloud Storage:**
   - AWS S3
   - Cloudinary
   - Azure Blob Storage

2. **Update Backend Code:**
   Replace local file storage with cloud storage SDK

### OCR Limitations

Tesseract OCR may not work on Vercel serverless. Options:

1. **Use External OCR Service:**
   - Google Cloud Vision API
   - AWS Textract
   - Azure Computer Vision

2. **Deploy Backend to Railway/Render:**
   These platforms support full system packages

## Alternative: Deploy Backend to Railway

If OCR doesn't work on Vercel:

```bash
cd server

# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Deploy
railway up
```

Configure environment variables in Railway dashboard.

## Troubleshooting

### Backend Issues

**Database Connection Fails:**
- Verify connection string format
- Check SSL mode is enabled
- Test connection locally first

**OCR Not Working:**
- Consider external OCR API
- Or deploy to Railway/Render

### Frontend Issues

**API Calls Fail:**
- Check NEXT_PUBLIC_API_URL is correct
- Verify CORS settings in backend
- Check browser console for errors

**Build Fails:**
- Clear build cache in Vercel
- Check for TypeScript errors
- Verify all dependencies are in package.json

## Monitoring

### Vercel Analytics

Enable in project settings:
- Web Analytics
- Speed Insights
- Error tracking

### Database Monitoring

- Neon/Supabase have built-in dashboards
- Monitor connection pool
- Check query performance

## Custom Domain (Optional)

### Frontend

1. Go to project → Settings → Domains
2. Add your domain
3. Configure DNS (follow Vercel instructions)

### Backend

1. Add domain in project settings
2. Update frontend NEXT_PUBLIC_API_URL
3. Update ALLOWED_ORIGINS in backend

## Costs

### Free Tier Limits

**Vercel:**
- Frontend: Unlimited bandwidth
- Backend: 100GB-hrs compute/month
- Serverless function timeout: 10s (Hobby), 60s (Pro)

**Neon (Database):**
- 1 project
- 10 GB storage
- Unlimited queries

For production, consider upgrading plans.

## Security Checklist

- [ ] Environment variables set correctly
- [ ] CORS configured properly
- [ ] Database connection uses SSL
- [ ] No sensitive data in code
- [ ] API rate limiting enabled (future)
- [ ] File upload validation working

## Next Steps

1. Add authentication (NextAuth.js)
2. Implement rate limiting
3. Add comprehensive logging
4. Set up CI/CD pipeline
5. Configure monitoring alerts

---

For support, refer to main README.md or open an issue.
