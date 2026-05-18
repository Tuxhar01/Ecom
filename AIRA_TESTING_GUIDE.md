# 🧪 AIRA Testing Guide - Production Deployment

## ✅ Current Status

Based on your Render logs:
```
[AIRA] Initializing handler...
[AIRA] Webhook URL: https://aira-1-yxlx.onrender.com//webhook
[AIRA] Enabled: True
[AIRA] Successfully initialized. Ready to send errors to https://aira-1-yxlx.onrender.com//webhook
[AIRA] Handler added to root logger and app logger
```

**AIRA is initialized and ready!** ✅

---

## ⚠️ Issue Found: Double Slash in Webhook URL

Your webhook URL has a double slash: `https://aira-1-yxlx.onrender.com//webhook`

This might cause issues. Check your Render environment variable:
- Current: `https://aira-1-yxlx.onrender.com//webhook`
- Should be: `https://aira-1-yxlx.onrender.com/webhook`

**Fix in Render Dashboard:**
1. Go to Environment Variables
2. Find `AIRA_WEBHOOK_URL`
3. Change to: `https://aira-1-yxlx.onrender.com/webhook` (single slash)
4. Save and redeploy

---

## 🎯 Correct Test URLs

### ❌ Wrong URLs (404 errors in your logs):
```
/test/error/auth          → 404
/test/error/database      → 404
/books?page=1             → 404
```

### ✅ Correct URLs:
```
https://ecom-backend-rne4.onrender.com/api/test/error/auth
https://ecom-backend-rne4.onrender.com/api/test/error/database
https://ecom-backend-rne4.onrender.com/api/test/error/generic
https://ecom-backend-rne4.onrender.com/api/books?page=1&per_page=20
```

**Note:** All API routes require the `/api/` prefix!

---

## 🧪 Testing Steps

### 1. Test Authentication Error (P1)
```bash
curl https://ecom-backend-rne4.onrender.com/api/test/error/auth
```

**Expected Response:**
```json
{
  "error": "Authentication failed",
  "severity": "P1",
  "message": "Invalid or expired JWT token"
}
```

**Expected in Render Logs:**
```
[AIRA] emit() called - enabled: True, level: ERROR
[AIRA] Processing error: Authentication failed: Invalid or expired JWT token
[AIRA] Payload built, sending to https://aira-1-yxlx.onrender.com/webhook
[AIRA] Attempting to send to webhook...
[AIRA] Attempt 1/3
[AIRA] Response status: 200
[AIRA] Successfully sent error to AIRA
```

### 2. Test Database Error (P0)
```bash
curl https://ecom-backend-rne4.onrender.com/api/test/error/database
```

**Expected Response:**
```json
{
  "error": "Database connection failed",
  "severity": "P0",
  "message": "Connection to database timed out"
}
```

### 3. Test Generic Error (P2)
```bash
curl https://ecom-backend-rne4.onrender.com/api/test/error/generic
```

**Expected Response:**
```json
{
  "error": "Something went wrong",
  "severity": "P2",
  "message": "An unexpected error occurred"
}
```

### 4. Test Validation Error (P2)
```bash
curl -X POST https://ecom-backend-rne4.onrender.com/api/test/error/validation \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid-email"}'
```

**Expected Response:**
```json
{
  "error": "Validation failed",
  "severity": "P2",
  "message": "Invalid email format"
}
```

---

## 🔍 Debugging in Browser

### Open Browser Console
1. Go to: `https://ecom-navy-three.vercel.app/`
2. Open DevTools (F12)
3. Go to Console tab
4. Run these commands:

```javascript
// Test auth error
fetch('https://ecom-backend-rne4.onrender.com/api/test/error/auth')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

// Test database error
fetch('https://ecom-backend-rne4.onrender.com/api/test/error/database')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

// Test generic error
fetch('https://ecom-backend-rne4.onrender.com/api/test/error/generic')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

---

## 📊 Verify in AIRA Dashboard

After triggering errors, check your AIRA dashboard:

### Expected Incidents:

**1. Authentication Error (P1)**
- Title: "Authentication failed: Invalid or expired JWT token"
- Severity: P1
- Stack trace included
- Request context: GET /api/test/error/auth

**2. Database Error (P0)**
- Title: "Database connection failed: Connection to database timed out"
- Severity: P0
- Stack trace included
- Request context: GET /api/test/error/database

**3. Generic Error (P2)**
- Title: "Something went wrong: An unexpected error occurred"
- Severity: P2
- Stack trace included
- Request context: GET /api/test/error/generic

---

## 🐛 Troubleshooting

### Issue: Still getting 404 errors
**Cause:** Missing `/api/` prefix in URL  
**Solution:** Always use `/api/` prefix for all routes

### Issue: No `[AIRA]` logs after error
**Cause:** Error not reaching logger  
**Solution:** Check if route is actually being hit (should see error in logs first)

### Issue: `[AIRA]` logs show "Failed to send"
**Cause:** AIRA backend not accessible or webhook URL wrong  
**Solution:** 
1. Fix double slash in webhook URL
2. Verify AIRA backend is running
3. Test webhook directly:
```bash
curl -X POST https://aira-1-yxlx.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Issue: Webhook returns 404
**Cause:** Wrong webhook endpoint  
**Solution:** Check AIRA backend logs for correct endpoint path

---

## 📝 Quick Checklist

Before testing, verify:

- [ ] AIRA backend is running and accessible
- [ ] Webhook URL in Render is correct (no double slash)
- [ ] Using correct URLs with `/api/` prefix
- [ ] Render logs show AIRA initialization
- [ ] AIRA dashboard is accessible

---

## 🎯 Expected Flow

```
1. User hits: /api/test/error/auth
   ↓
2. Route handler raises AuthenticationError
   ↓
3. Logger captures error (routes.test_routes)
   ↓
4. Error propagates to root logger
   ↓
5. AIRA handler's emit() is called
   ↓
6. Payload is built with context
   ↓
7. HTTP POST to AIRA webhook
   ↓
8. AIRA receives and creates incident
   ↓
9. Incident appears in AIRA dashboard
```

---

## 🚀 Production Testing Commands

Copy and paste these to test all error types:

```bash
# Test all error endpoints
echo "Testing Authentication Error..."
curl https://ecom-backend-rne4.onrender.com/api/test/error/auth
echo -e "\n\nTesting Database Error..."
curl https://ecom-backend-rne4.onrender.com/api/test/error/database
echo -e "\n\nTesting Generic Error..."
curl https://ecom-backend-rne4.onrender.com/api/test/error/generic
echo -e "\n\nTesting Validation Error..."
curl -X POST https://ecom-backend-rne4.onrender.com/api/test/error/validation \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid"}'
```

After running these, check:
1. ✅ Render logs for `[AIRA]` messages
2. ✅ AIRA dashboard for new incidents
3. ✅ Each incident has proper severity (P0/P1/P2)

---

## 📞 Support

If errors still don't appear in AIRA:

1. **Share Render logs** (filter by `[AIRA]`)
2. **Share AIRA backend logs**
3. **Test webhook directly** with curl
4. **Verify network connectivity** between Render and AIRA

---

*Generated by Bob - Code Mode*