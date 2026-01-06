# Vercel Environment Variables Setup

## The Build Error You Encountered

The error occurred because `NEXT_PUBLIC_API_URL` was not defined during the Vercel build:
```
`destination` does not start with `/`, `http://`, or `https://` for route {"source":"/api/:path*","destination":"undefined/api/:path*"}
```

## Solution Implemented

✅ **Fixed `next.config.ts`** to provide a fallback value during build, preventing the error.

## Required: Set Environment Variable in Vercel

For your application to work correctly in production, you **must** set the environment variable in Vercel:

### Step-by-Step Instructions

1. **Go to Your Vercel Project Dashboard**
   - Visit: https://vercel.com/dashboard
   - Select your `document_reader` project

2. **Navigate to Environment Variables**
   - Click on **Settings** tab
   - Click on **Environment Variables** in the sidebar

3. **Add the Environment Variable**
   - **Key**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend API URL
     - If backend is on Vercel: `https://your-backend-project.vercel.app`
     - If backend is elsewhere: `https://your-backend-domain.com`
   - **Environments**: Select all (Production, Preview, Development)

4. **Redeploy**
   - After saving the environment variable
   - Go to **Deployments** tab
   - Click the **...** menu on the latest deployment
   - Select **Redeploy**

## Important Notes

### Backend URL Requirements

- Must be the **full URL** including protocol (https://)
- Should **NOT** end with a slash
- Example: `https://document-reader-api.vercel.app`

### CORS Configuration

Make sure your backend's `ALLOWED_ORIGINS` includes your frontend URL:
```
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-frontend-git-main.vercel.app
```

### If You Don't Have a Backend Yet

If you haven't deployed your backend:

1. **Deploy the backend first**:
   - The server folder contains the FastAPI backend
   - Follow `DEPLOYMENT.md` for backend deployment instructions
   - Note the deployed backend URL

2. **Then set the frontend environment variable** with that URL

3. **Finally, redeploy the frontend**

## Quick Verification

After redeploying, check:
1. Build logs show no errors
2. Visit your site and open browser DevTools → Network
3. API calls should go to your backend URL
4. Check Console for any CORS or connection errors

## Local Development

For local development, create `client/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This file is gitignored and won't affect Vercel deployments.

---

**Need Help?** 
- Check `DEPLOYMENT.md` for full deployment guide
- See `TROUBLESHOOTING_FETCH_ERROR.md` for API connection issues
