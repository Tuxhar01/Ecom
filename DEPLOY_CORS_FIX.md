# Deploy CORS Fix to Render - Step by Step Guide

## Current Situation
✅ **Local backend** - CORS fix applied and working
❌ **Production backend (Render)** - Still has old code, causing 404 errors

## Why You're Getting 404 Errors

Your frontend at `https://ecom-navy-three.vercel.app` is trying to access:
```
https://ecom-backend-rne4.onrender.com/api/books
```

But your **deployed backend on Render** still has the old code without the CORS fix.

## Solution: Deploy Updated Code to Render

### Option 1: Push to Git (Recommended)

If your Render service is connected to a Git repository:

```bash
# 1. Check git status
git status

# 2. Add all changes
git add .

# 3. Commit with a clear message
git commit -m "Fix CORS configuration for production deployment"

# 4. Push to your main branch
git push origin main
```

Render will automatically detect the push and redeploy your backend.

### Option 2: Manual Deploy via Render Dashboard

1. Go to https://dashboard.render.com/
2. Find your service: **ecom-backend-rne4**
3. Click on the service
4. Click **"Manual Deploy"** button
5. Select **"Deploy latest commit"**
6. Wait for deployment to complete (usually 2-5 minutes)

### Option 3: Connect to Git Repository (If Not Connected)

If your Render service isn't connected to Git:

1. Go to https://dashboard.render.com/
2. Click on **ecom-backend-rne4** service
3. Go to **Settings** tab
4. Under **Build & Deploy**, connect your GitHub/GitLab repository
5. Set branch to `main`
6. Enable **Auto-Deploy**
7. Click **Save Changes**
8. Trigger a manual deploy

## Important: Set Environment Variables on Render

Before or after deploying, ensure these environment variables are set:

1. Go to your service on Render dashboard
2. Click **Environment** tab
3. Add/Update these variables:

```
FRONTEND_URL=https://ecom-navy-three.vercel.app
FLASK_SECRET_KEY=<your-secret-key>
JWT_SECRET_KEY=<your-jwt-secret>
AIRA_WEBHOOK_URL=https://unbuckled-immorally-semester.ngrok-free.dev/webhook
AIRA_API_KEY=aira_j3G7xC_Qoiwn1f0JEG_B-vBhLiFQUQ67ZkVB81axdPc
FLASK_ENV=production
```

4. Click **Save Changes**

## Verify Deployment

### Step 1: Check Render Logs

1. Go to your service on Render
2. Click **Logs** tab
3. Look for:
   ```
   Bookstore API with AIRA Integration
   Server: http://0.0.0.0:10000
   AIRA Enabled: True
   ```

### Step 2: Test Health Endpoint

Open browser console and run:
```javascript
fetch('https://ecom-backend-rne4.onrender.com/health')
  .then(r => r.json())
  .then(console.log);
```

Should return:
```json
{
  "status": "healthy",
  "aira_enabled": true
}
```

### Step 3: Test Books Endpoint

```javascript
fetch('https://ecom-backend-rne4.onrender.com/api/books?page=1&per_page=10')
  .then(r => r.json())
  .then(console.log);
```

Should return:
```json
{
  "books": [...],
  "total": 20,
  "page": 1,
  "per_page": 10,
  "pages": 2
}
```

### Step 4: Test from Your Frontend

1. Open https://ecom-navy-three.vercel.app
2. Open browser console (F12)
3. Try browsing books or logging in
4. Should see NO CORS errors

## Troubleshooting

### Issue: Render shows "Build failed"

**Check:**
- `requirements.txt` is in the `backend/` directory
- All dependencies are listed correctly
- Python version is compatible (3.9+)

**Solution:**
```bash
cd backend
pip install -r requirements.txt  # Test locally first
```

### Issue: Render shows "Deploy succeeded" but still 404

**Possible causes:**
1. Environment variables not set
2. Wrong branch deployed
3. Cache issue

**Solution:**
1. Clear build cache: Settings → Clear build cache
2. Redeploy: Manual Deploy → Deploy latest commit
3. Check logs for startup errors

### Issue: CORS errors still appear

**Check:**
1. Is `FRONTEND_URL` set correctly on Render?
2. Did the deployment actually complete?
3. Are you testing the right URL?

**Solution:**
```bash
# Check what's deployed
curl -I https://ecom-backend-rne4.onrender.com/health

# Should include CORS headers:
# Access-Control-Allow-Origin: *
```

### Issue: "Service Unavailable" or takes long to respond

**Cause:** Render free tier services sleep after 15 minutes of inactivity

**Solution:** 
- First request wakes up the service (takes 30-60 seconds)
- Subsequent requests are fast
- Consider upgrading to paid tier for always-on service

## Quick Deployment Checklist

- [ ] Code changes committed locally
- [ ] Git repository up to date
- [ ] Environment variables set on Render
- [ ] Deployment triggered (auto or manual)
- [ ] Deployment completed successfully
- [ ] Health endpoint returns 200
- [ ] Books endpoint returns data
- [ ] Frontend can access backend
- [ ] No CORS errors in browser console

## Expected Timeline

- **Git push to deployment start:** Immediate (if auto-deploy enabled)
- **Build time:** 2-3 minutes
- **Deploy time:** 1-2 minutes
- **Total:** ~5 minutes from push to live

## After Successful Deployment

Your frontend should work perfectly:
- ✅ No CORS errors
- ✅ Can browse books
- ✅ Can register/login
- ✅ Can add to cart
- ✅ Can place orders

## Need Help?

If deployment fails or issues persist:

1. **Check Render logs** for specific error messages
2. **Test locally** to ensure code works
3. **Verify environment variables** are set correctly
4. **Clear cache** and redeploy
5. **Check this guide** for troubleshooting steps

---

Made with Bob 🤖