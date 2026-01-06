# Backend Deployment Guide

## Your Database Information
- **Provider**: Neon PostgreSQL
- **Connection String**: `postgresql://neondb_owner:npg_vlSVX8gNGE1D@ep-fragrant-hat-a1wl29ds-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`

## Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway is perfect for Python apps with heavy dependencies like OCR.

#### Steps:

1. **Create Railway Account**
   - Go to: https://railway.app/
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `document_reader` repository
   - Railway will auto-detect it's a Python project

3. **Configure Root Directory**
   - In Railway dashboard, go to Settings
   - Set "Root Directory" to `server`
   - Railway will use the `railway.json` configuration

4. **Set Environment Variables**
   Click on "Variables" tab and add:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_vlSVX8gNGE1D@ep-fragrant-hat-a1wl29ds-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ALLOWED_ORIGINS=https://document-reader-chi.vercel.app
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=<your-secure-password>
   JWT_SECRET_KEY=<generate-a-random-string>
   DEBUG=False
   TESSERACT_CMD=/usr/bin/tesseract
   ```

5. **Generate Secure Values**
   For `JWT_SECRET_KEY`, run this in your terminal:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

6. **Deploy**
   - Railway will automatically deploy
   - You'll get a URL like: `https://your-app.up.railway.app`

7. **Enable Public Domain**
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Copy your public URL

### Option 2: Render

Render offers a free tier and good support for system dependencies.

#### Steps:

1. **Create Render Account**
   - Go to: https://render.com/
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `document_reader`

3. **Configure Service**
   - **Name**: document-reader-api
   - **Root Directory**: `server`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add System Dependencies**
   - In "Advanced" settings, add these shell commands to run before build:
   ```bash
   apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng
   ```

5. **Set Environment Variables**
   Add these in the "Environment" section:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_vlSVX8gNGE1D@ep-fragrant-hat-a1wl29ds-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ALLOWED_ORIGINS=https://document-reader-chi.vercel.app
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=<your-secure-password>
   JWT_SECRET_KEY=<generate-a-random-string>
   DEBUG=False
   TESSERACT_CMD=/usr/bin/tesseract
   PORT=10000
   ```

6. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy
   - You'll get a URL like: `https://document-reader-api.onrender.com`

## After Deployment

### 1. Update Frontend Environment Variable

Once your backend is deployed, update Vercel:

1. Go to: https://vercel.com/dashboard
2. Select your `document-reader-chi` project
3. Go to Settings → Environment Variables
4. Add or update:
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://your-backend-url.up.railway.app` (or Render URL)
   - **Environments**: Production, Preview, Development
5. Redeploy the frontend

### 2. Initialize Database

Your Neon database needs tables created. After deploying the backend:

**Option A: Using the API endpoint (if you added one)**
```bash
curl -X POST https://your-backend-url/api/init-db
```

**Option B: Connect directly to Neon and run migrations**
```bash
psql "postgresql://neondb_owner:npg_vlSVX8gNGE1D@ep-fragrant-hat-a1wl29ds-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
```

Then run your table creation SQL or use SQLAlchemy's `create_all()`.

### 3. Test the Deployment

1. **Check Backend Health**:
   ```bash
   curl https://your-backend-url/
   ```
   Should return: `{"message": "NED University Document Management System API"}`

2. **Test Login**:
   ```bash
   curl -X POST https://your-backend-url/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"your-password"}'
   ```

3. **Visit Frontend**:
   - Go to: https://document-reader-chi.vercel.app
   - Try logging in
   - Test upload functionality

## Troubleshooting

### Backend won't start
- Check logs in Railway/Render dashboard
- Verify all environment variables are set
- Ensure `DATABASE_URL` is correct

### CORS Errors
- Make sure `ALLOWED_ORIGINS` includes your exact Vercel URL
- Include both `https://document-reader-chi.vercel.app` and any preview URLs

### Database Connection Issues
- Verify Neon database is active
- Check if IP restrictions are set in Neon (should allow all for connection pooler)
- Test connection string directly with psql

### Tesseract Not Found
- Railway: Should install automatically
- Render: Add the apt-get command in build settings
- Verify `TESSERACT_CMD=/usr/bin/tesseract` is set

## Cost Information

### Railway
- **Free Tier**: $5 credit monthly (hobby plan)
- **Paid**: Pay-as-you-go after free tier
- Good for: Development and moderate production use

### Render
- **Free Tier**: Available but with sleep on inactivity
- **Paid**: Starts at $7/month for always-on
- Good for: Development or production with predictable costs

### Neon Database
- **Free Tier**: 0.5 GB storage, 3 GB data transfer
- **Paid**: Starts at $19/month
- You're already set up with this!

## Security Checklist

✅ Change default admin password  
✅ Generate secure JWT secret key  
✅ Set DEBUG=False in production  
✅ Configure CORS to only allow your frontend domain  
✅ Use connection pooler for database (you already are!)  
✅ Enable HTTPS (automatic on Railway/Render)  

## Need Help?

- Railway Discord: https://discord.gg/railway
- Render Community: https://community.render.com/
- This project's issues: https://github.com/syedzainalii/document_reader/issues
