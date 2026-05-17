# CORS Error Fix Guide

## Understanding the Error

### What is CORS?
CORS (Cross-Origin Resource Sharing) is a security feature implemented by browsers that restricts web pages from making requests to a different domain than the one serving the web page.

### Your Error Explained:
```
Access to XMLHttpRequest at 'https://ecom-backend-rne4.onrender.com/books?page=1&per_page=20&search=' 
from origin 'https://ecom-navy-three.vercel.app' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**What this means:**
1. Your frontend is hosted at: `https://ecom-navy-three.vercel.app`
2. Your backend is hosted at: `https://ecom-backend-rne4.onrender.com`
3. The browser blocked the request because the backend didn't send proper CORS headers
4. The backend needs to explicitly allow requests from your frontend domain

## The Fix Applied

### 1. Updated CORS Configuration in `backend/app.py`

**Before:**
```python
CORS(app, resources={
    r"/api/*": {
        "origins": Config.FRONTEND_URL,
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

**After:**
```python
CORS(app, 
     resources={r"/*": {"origins": "*"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type", "Authorization"])
```

**Changes Made:**
- ✅ Changed from `/api/*` to `/*` to allow all routes
- ✅ Set `origins: "*"` to allow all origins (for development/testing)
- ✅ Added `supports_credentials=True` for JWT authentication
- ✅ Added proper headers for preflight requests (OPTIONS)
- ✅ Added `Access-Control-Allow-Credentials` header

### 2. Updated `.env` File

Changed `FRONTEND_URL` from `http://localhost:5173` to `https://ecom-navy-three.vercel.app`

## Deployment Steps for Render

### Step 1: Update Environment Variables on Render

1. Go to your Render dashboard: https://dashboard.render.com/
2. Select your backend service: `ecom-backend-rne4`
3. Go to **Environment** tab
4. Add/Update these environment variables:

```
FRONTEND_URL=https://ecom-navy-three.vercel.app
FLASK_SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-here-change-in-production
AIRA_WEBHOOK_URL=https://unbuckled-immorally-semester.ngrok-free.dev/webhook
AIRA_API_KEY=aira_j3G7xC_Qoiwn1f0JEG_B-vBhLiFQUQ67ZkVB81axdPc
DATABASE_URL=sqlite:///bookstore.db
```

### Step 2: Deploy the Updated Code

**Option A: Manual Deploy**
1. In Render dashboard, click **Manual Deploy** → **Deploy latest commit**

**Option B: Git Push (if auto-deploy is enabled)**
```bash
git add .
git commit -m "Fix CORS configuration for production"
git push origin main
```

### Step 3: Verify the Fix

After deployment, test these endpoints in your browser console:

```javascript
// Test 1: Books endpoint
fetch('https://ecom-backend-rne4.onrender.com/api/books?page=1&per_page=20')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

// Test 2: Health endpoint
fetch('https://ecom-backend-rne4.onrender.com/health')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

## Security Considerations

### Current Configuration (Development/Testing)
```python
origins: "*"  # Allows ALL origins
```

### Recommended for Production
For better security, restrict to specific origins:

```python
CORS(app, 
     resources={r"/*": {
         "origins": [
             "https://ecom-navy-three.vercel.app",
             "http://localhost:5173"  # For local development
         ]
     }},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type", "Authorization"])
```

## Troubleshooting

### If CORS errors persist:

1. **Clear browser cache and hard reload** (Ctrl+Shift+R or Cmd+Shift+R)

2. **Check Render logs:**
   - Go to Render dashboard → Your service → Logs
   - Look for startup messages and errors

3. **Verify environment variables:**
   - Ensure `FRONTEND_URL` is set correctly on Render
   - Check that all required variables are present

4. **Test with curl:**
   ```bash
   curl -H "Origin: https://ecom-navy-three.vercel.app" \
        -H "Access-Control-Request-Method: GET" \
        -H "Access-Control-Request-Headers: Content-Type" \
        -X OPTIONS \
        https://ecom-backend-rne4.onrender.com/api/books
   ```
   
   Should return headers including:
   ```
   Access-Control-Allow-Origin: *
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
   ```

5. **Check if backend is running:**
   ```bash
   curl https://ecom-backend-rne4.onrender.com/health
   ```

### Common Issues:

**Issue 1: "Failed to load resource: net::ERR_FAILED"**
- Backend might be sleeping (Render free tier)
- Solution: Wait 30-60 seconds for backend to wake up

**Issue 2: "Response to preflight request doesn't pass access control check"**
- OPTIONS method not properly configured
- Solution: Already fixed in the updated CORS config

**Issue 3: Backend returns 404**
- Route path mismatch
- Solution: Verify your routes use `/api/` prefix (already correct)

## Testing Locally

To test the CORS fix locally:

1. **Start backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Start frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test in browser:**
   - Open http://localhost:5173
   - Open browser console (F12)
   - Try logging in or browsing books
   - Should see no CORS errors

## Next Steps

1. ✅ CORS configuration updated
2. ✅ Environment variables documented
3. 🔄 **Deploy to Render** (you need to do this)
4. 🔄 **Test production frontend** (after deployment)
5. 🔄 **Consider restricting origins** for production security

## Summary

**What was wrong:**
- CORS only allowed `/api/*` routes but routes are registered at `/api/books`, `/api/auth`, etc.
- Frontend URL in `.env` was set to localhost instead of production URL
- Missing proper CORS headers for preflight requests

**What was fixed:**
- Changed CORS to allow all routes (`/*`)
- Set `origins: "*"` to allow all origins (can be restricted later)
- Added proper headers for authentication and preflight requests
- Updated `.env` with production frontend URL

**What you need to do:**
1. Set environment variables on Render
2. Deploy the updated code
3. Test your production frontend

---

Made with Bob 🤖