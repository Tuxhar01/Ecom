# 🔍 AIRA Deployment Debugging Guide

## Issue Identified

**Problem:** AIRA handler is initialized but not capturing errors from route loggers.

**Root Cause:** The test routes use `routes.test_routes` logger, which is a child logger that wasn't getting the AIRA handler attached.

---

## Fix Applied

### Updated `backend/aira_handler.py`

**Changes:**
1. ✅ Added comprehensive debug logging with `[AIRA]` prefix
2. ✅ Set root logger level to ERROR to ensure it captures all error logs
3. ✅ Ensured AIRA handler is added to root logger FIRST (catches all child loggers)
4. ✅ Added explicit level setting for app logger

**Key Code:**
```python
# Add to root logger first - this catches ALL loggers
root_logger = logging.getLogger()
root_logger.addHandler(aira_handler)
root_logger.setLevel(logging.ERROR)  # Ensure root logger captures errors

# Also add to app logger for good measure
app.logger.addHandler(aira_handler)
app.logger.setLevel(logging.ERROR)
```

---

## Deployment Steps

### 1. Commit and Push Changes
```bash
git add backend/aira_handler.py
git commit -m "Fix AIRA handler: Ensure all loggers are captured"
git push origin main
```

### 2. Verify Render Environment Variables
In Render Dashboard → Environment:
```
AIRA_WEBHOOK_URL=https://aira-1-yxlx.onrender.com/webhook
AIRA_ENABLED=true
```

### 3. Redeploy on Render
- Render will auto-deploy after push
- Or manually trigger: Dashboard → Manual Deploy → Deploy latest commit

### 4. Check Logs After Deployment
Look for these `[AIRA]` messages in Render logs:
```
[AIRA] Initializing handler...
[AIRA] Webhook URL: https://aira-1-yxlx.onrender.com/webhook
[AIRA] Enabled: True
[AIRA] Successfully initialized. Ready to send errors to https://aira-1-yxlx.onrender.com/webhook
[AIRA] Handler added to root logger and app logger
```

### 5. Test Error Logging
Trigger a test error:
```bash
# Visit this URL in browser or curl
https://your-app.onrender.com/api/test/error/auth
```

Expected logs:
```
[AIRA] emit() called - enabled: True, level: ERROR
[AIRA] Processing error: Authentication failed: Invalid or expired JWT token
[AIRA] Payload built, sending to https://aira-1-yxlx.onrender.com/webhook
[AIRA] Attempting to send to webhook: https://aira-1-yxlx.onrender.com/webhook
[AIRA] Attempt 1/3
[AIRA] Response status: 200
[AIRA] Successfully sent error to AIRA
```

---

## Debugging Checklist

### ✅ Environment Configuration
- [ ] `AIRA_WEBHOOK_URL` is set in Render
- [ ] `AIRA_ENABLED=true` in Render
- [ ] AIRA backend is accessible from Render (test with curl)

### ✅ Code Deployment
- [ ] Latest code is pushed to GitHub
- [ ] Render has deployed the latest commit
- [ ] No build errors in Render logs

### ✅ Handler Initialization
- [ ] See `[AIRA] Initializing handler...` in logs
- [ ] See `[AIRA] Successfully initialized...` in logs
- [ ] See `[AIRA] Handler added to root logger...` in logs

### ✅ Error Capture
- [ ] Trigger test error endpoint
- [ ] See `[AIRA] emit() called...` in logs
- [ ] See `[AIRA] Processing error...` in logs
- [ ] See `[AIRA] Successfully sent error to AIRA` in logs

### ✅ AIRA Backend
- [ ] AIRA backend is running
- [ ] AIRA webhook endpoint is accessible
- [ ] Check AIRA dashboard for received incidents

---

## Common Issues & Solutions

### Issue 1: No `[AIRA]` logs at all
**Cause:** Old code still deployed  
**Solution:** 
```bash
git push origin main
# Wait for Render to redeploy
# Check deployment logs
```

### Issue 2: `[AIRA] Initializing...` but no `emit()` calls
**Cause:** Root logger level not set correctly  
**Solution:** ✅ Already fixed - root logger level set to ERROR

### Issue 3: `[AIRA] emit() called` but `enabled: False`
**Cause:** `AIRA_ENABLED` not set or webhook URL missing  
**Solution:** Check Render environment variables

### Issue 4: Webhook calls failing (timeout/connection error)
**Cause:** AIRA backend not accessible from Render  
**Solution:** 
- Verify AIRA backend is running
- Test webhook URL: `curl https://aira-1-yxlx.onrender.com/webhook`
- Check AIRA backend logs

### Issue 5: Response status 404 or 500
**Cause:** AIRA webhook endpoint issue  
**Solution:** Check AIRA backend logs and endpoint configuration

---

## Testing Locally

### 1. Set Environment Variables
```bash
# In backend/.env
AIRA_WEBHOOK_URL=https://aira-1-yxlx.onrender.com/webhook
AIRA_ENABLED=true
```

### 2. Run Backend
```bash
cd backend
python app.py
```

### 3. Check Initialization Logs
Should see:
```
[AIRA] Initializing handler...
[AIRA] Webhook URL: https://aira-1-yxlx.onrender.com/webhook
[AIRA] Enabled: True
[AIRA] Successfully initialized...
[AIRA] Handler added to root logger and app logger
```

### 4. Trigger Test Error
```bash
curl http://localhost:5000/api/test/error/auth
```

### 5. Verify in Logs
Should see:
```
[AIRA] emit() called - enabled: True, level: ERROR
[AIRA] Processing error: Authentication failed...
[AIRA] Attempting to send to webhook...
[AIRA] Response status: 200
[AIRA] Successfully sent error to AIRA
```

### 6. Check AIRA Dashboard
- Open AIRA dashboard
- Should see new incident
- Verify incident details (stack trace, context, etc.)

---

## Verification Commands

### Check if AIRA backend is accessible
```bash
curl -X POST https://aira-1-yxlx.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Check Render logs
```bash
# In Render dashboard:
# Logs → Filter by "[AIRA]"
```

### Test error endpoint
```bash
# Authentication error
curl https://your-app.onrender.com/api/test/error/auth

# Database error
curl https://your-app.onrender.com/api/test/error/database

# Generic error
curl https://your-app.onrender.com/api/test/error/generic
```

---

## Expected Behavior After Fix

### On Application Start
```
[AIRA] Initializing handler...
[AIRA] Webhook URL: https://aira-1-yxlx.onrender.com/webhook
[AIRA] Enabled: True
[AIRA] Successfully initialized. Ready to send errors to https://aira-1-yxlx.onrender.com/webhook
AIRA error monitoring initialized
[AIRA] Handler added to root logger and app logger
```

### On Error Occurrence
```
2026-05-18 12:37:23,945 - routes.test_routes - ERROR - Authentication failed: Invalid or expired JWT token
[AIRA] emit() called - enabled: True, level: ERROR
[AIRA] Processing error: Authentication failed: Invalid or expired JWT token
[AIRA] Payload built, sending to https://aira-1-yxlx.onrender.com/webhook
[AIRA] Attempting to send to webhook: https://aira-1-yxlx.onrender.com/webhook
[AIRA] Attempt 1/3
[AIRA] Response status: 200
[AIRA] Successfully sent error to AIRA
```

### In AIRA Dashboard
- New incident created
- Severity: P1 (for auth errors)
- Stack trace included
- Request context included
- User information (if authenticated)

---

## Next Steps

1. **Deploy the fix:**
   ```bash
   git add backend/aira_handler.py AIRA_DEPLOYMENT_DEBUG.md
   git commit -m "Fix AIRA: Capture all logger errors + debug logging"
   git push origin main
   ```

2. **Wait for Render deployment** (2-3 minutes)

3. **Check Render logs** for `[AIRA]` initialization messages

4. **Trigger test error** and verify it appears in AIRA dashboard

5. **Monitor production** - all errors should now be captured

---

## Support

If issues persist after deployment:
1. Share Render logs (filter by `[AIRA]`)
2. Check AIRA backend logs
3. Verify network connectivity between Render and AIRA backend
4. Test webhook endpoint directly with curl

---

*Generated by Bob - Code Mode*