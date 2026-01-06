# 🚀 Quick Deployment Guide

## Current Status

✅ **Frontend Deployed**: https://document-reader-chi.vercel.app/  
⏳ **Backend**: Ready to deploy  
✅ **Database**: Neon PostgreSQL configured  

## Next Steps (Choose One Platform)

### Option A: Deploy to Railway (Recommended - Easiest)

1. **Go to Railway**
   - Visit: https://railway.app/
   - Sign up/login with GitHub

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `syedzainalii/document_reader`
   - Railway auto-detects Python

3. **Configure Settings**
   - Click Settings → Set "Root Directory" to `server`
   - Railway will use the `railway.json` config automatically

4. **Add Environment Variables**
   Click "Variables" tab and paste these:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_vlSVX8gNGE1D@ep-fragrant-hat-a1wl29ds-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ALLOWED_ORIGINS=https://document-reader-chi.vercel.app
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=SecurePassword123!
   JWT_SECRET_KEY=your-random-secret-key-here
   DEBUG=False
   TESSERACT_CMD=/usr/bin/tesseract
   ```

   **Generate JWT Secret**: Run this command locally:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Deploy**
   - Railway will automatically build and deploy
   - Get your URL: Settings → Networking → Generate Domain
   - Example: `https://document-reader-api.up.railway.app`

6. **Copy Your Backend URL** for the next step

---

### Option B: Deploy to Render

1. **Go to Render**
   - Visit: https://render.com/
   - Sign up/login with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect `syedzainalii/document_reader`

3. **Configure**
   - **Name**: document-reader-api
   - **Root Directory**: `server`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

4. **Add System Dependencies**
   - Expand "Advanced" settings
   - Add Pre-Deploy Command:
   ```bash
   apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng
   ```

5. **Set Environment Variables**
   Same as Railway (see above)

6. **Deploy**
   - Click "Create Web Service"
   - Get your URL like: `https://document-reader-api.onrender.com`

---

## Step 2: Update Frontend (After Backend is Live)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Select `document_reader` project

2. **Add Environment Variable**
   - Settings → Environment Variables
   - Click "Add New"
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend URL (from Railway/Render)
     - Example: `https://document-reader-api.up.railway.app`
   - Select all environments: Production, Preview, Development

3. **Redeploy**
   - Go to Deployments tab
   - Click "..." on latest deployment → "Redeploy"

---

## Step 3: Initialize Database

After backend is deployed, initialize the database tables:

**Option 1: Automatic (on first request)**
- The backend automatically creates tables on startup
- Just try logging in at your frontend

**Option 2: Manual verification**
Visit your backend health endpoint:
```
https://your-backend-url/health
```

Should return: `{"status": "healthy", "timestamp": "..."}`

---

## Step 4: Test Your App

1. **Visit Frontend**: https://document-reader-chi.vercel.app/

2. **Login**
   - Username: `admin`
   - Password: (the one you set in environment variables)

3. **Test Features**
   - Upload a document
   - View students list
   - Check statistics

---

## Troubleshooting

### Backend won't start
- Check logs in Railway/Render dashboard
- Verify all environment variables are set correctly
- Check `DATABASE_URL` has `?sslmode=require` at the end

### CORS Errors (Frontend can't reach backend)
- Ensure `ALLOWED_ORIGINS` includes exact Vercel URL
- No trailing slash in the URL
- Include both main URL and preview URLs if needed

### Login not working
- Check browser console for errors
- Verify `NEXT_PUBLIC_API_URL` is set in Vercel
- Check backend logs for authentication errors

### Database connection failed
- Neon database must be active
- Connection string must be exact
- Check if Neon has IP restrictions (it shouldn't for pooler)

---

## Security Checklist

Before going to production:

- [ ] Changed `ADMIN_PASSWORD` from default
- [ ] Generated secure `JWT_SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Verified `ALLOWED_ORIGINS` only includes your domains
- [ ] Tested login and authentication
- [ ] Backed up database (Neon handles this)

---

## Cost Estimates

**Railway**: $5 free credit/month → ~$10-15/month for light usage  
**Render**: Free tier available → $7/month for production  
**Vercel**: Free for hobby projects  
**Neon**: 0.5 GB free → $19/month for more  

---

## Need Help?

1. Check `server/DEPLOYMENT_GUIDE.md` for detailed instructions
2. Railway Discord: https://discord.gg/railway
3. Render Community: https://community.render.com/

---

## Quick Commands Reference

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Test Backend Health:**
```bash
curl https://your-backend-url/health
```

**Test Login:**
```bash
curl -X POST https://your-backend-url/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your-password"}'
```

**View Backend Logs:**
- Railway: Project → View Logs
- Render: Dashboard → Logs tab
