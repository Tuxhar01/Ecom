# 🚀 Render Deployment Guide - E-Commerce Backend

Complete step-by-step guide to deploy your Flask backend on Render.

---

## 📋 Prerequisites

- GitHub account with repository: https://github.com/Tuxhar01/Ecom.git
- Render account (sign up at https://render.com)
- AIRA webhook URL and API key

---

## 🎯 Deployment Methods

### Method 1: Using Render Dashboard (Recommended - Easiest)

#### Step 1: Sign Up / Login to Render
1. Go to https://render.com
2. Sign up with GitHub (recommended) or email
3. Authorize Render to access your GitHub repositories

#### Step 2: Create PostgreSQL Database
1. Click **"New +"** button
2. Select **"PostgreSQL"**
3. Configure database:
   - **Name**: `ecom-db`
   - **Database**: `bookstore`
   - **User**: `bookstore_user`
   - **Region**: Choose closest to you (e.g., Oregon)
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait for database to be created (2-3 minutes)
6. **IMPORTANT**: Copy the **Internal Database URL** (starts with `postgresql://`)

#### Step 3: Create Web Service
1. Click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Select **"Tuxhar01/Ecom"**
   - Click **"Connect"**
4. Configure service:
   - **Name**: `ecom-backend`
   - **Region**: Same as database (Oregon)
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

#### Step 4: Add Environment Variables
Click **"Advanced"** and add these environment variables:

```
FLASK_SECRET_KEY = <click "Generate" button>
JWT_SECRET_KEY = <click "Generate" button>
FLASK_ENV = production
DATABASE_URL = <paste Internal Database URL from Step 2>
AIRA_WEBHOOK_URL = https://unbuckled-immorally-semester.ngrok-free.dev/webhook
AIRA_API_KEY = <your-aira-api-key>
FRONTEND_URL = https://your-frontend-url.vercel.app
```

#### Step 5: Deploy
1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application
3. Wait 5-10 minutes for first deployment
4. Your backend will be live at: `https://ecom-backend.onrender.com`

#### Step 6: Initialize Database
1. Go to your web service dashboard
2. Click **"Shell"** tab
3. Run these commands:
```bash
cd backend
python seed_data.py
```

#### Step 7: Test Your Deployment
```bash
# Test health endpoint
curl https://ecom-backend.onrender.com/api/health

# Test books endpoint
curl https://ecom-backend.onrender.com/api/books

# Test AIRA error logging
curl https://ecom-backend.onrender.com/api/test/error/database
```

---

### Method 2: Using render.yaml (Infrastructure as Code)

#### Step 1: Verify render.yaml
The `render.yaml` file is already in your repository root. It defines:
- Web service configuration
- PostgreSQL database
- Environment variables

#### Step 2: Deploy via Render Dashboard
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Review the configuration
6. Click **"Apply"**

#### Step 3: Set Manual Environment Variables
After deployment, go to your service and add:
- `AIRA_WEBHOOK_URL`
- `AIRA_API_KEY`
- `FRONTEND_URL`

---

### Method 3: Using Render CLI (Advanced)

#### Step 1: Install Render CLI
```bash
# Using npm
npm install -g @render/cli

# Or using pip
pip install render-cli
```

#### Step 2: Login to Render
```bash
render login
```

#### Step 3: Deploy from Command Line
```bash
# Navigate to project root
cd c:/Users/Tushar Kumar/Desktop/Ecom

# Deploy using render.yaml
render blueprint deploy
```

#### Step 4: Check Deployment Status
```bash
render services list
render logs ecom-backend
```

---

## 🔧 Post-Deployment Configuration

### Update Frontend API URL
Update your frontend to use the Render backend URL:

```typescript
// frontend/src/services/api.ts
const API_URL = 'https://ecom-backend.onrender.com';
```

### Update CORS Settings
Ensure your backend allows requests from your frontend:

```python
# backend/app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend.vercel.app"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Verify AIRA Integration
1. Trigger a test error:
```bash
curl https://ecom-backend.onrender.com/api/test/error/payment
```

2. Check AIRA dashboard for the error log

---

## 📊 Monitoring Your Deployment

### View Logs
1. Go to Render Dashboard
2. Select your service
3. Click **"Logs"** tab
4. Real-time logs will appear

### Check Metrics
1. Click **"Metrics"** tab
2. View:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

### Set Up Alerts
1. Click **"Settings"** tab
2. Scroll to **"Notifications"**
3. Add email or Slack webhook for alerts

---

## 🔄 Continuous Deployment

Render automatically deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin main

# Render will automatically:
# 1. Detect the push
# 2. Build your application
# 3. Deploy the new version
# 4. Zero-downtime deployment
```

---

## 🐛 Troubleshooting

### Issue: Build Failed
**Solution**: Check build logs in Render dashboard
```bash
# Common fixes:
# 1. Verify requirements.txt is correct
# 2. Check Python version compatibility
# 3. Ensure all imports are available
```

### Issue: Database Connection Error
**Solution**: Verify DATABASE_URL environment variable
```bash
# In Render Shell:
echo $DATABASE_URL

# Should start with: postgresql://
```

### Issue: AIRA Not Logging Errors
**Solution**: Check environment variables
```bash
# Verify in Render dashboard:
# - AIRA_WEBHOOK_URL is set
# - AIRA_API_KEY is set
# - Both are correct
```

### Issue: 502 Bad Gateway
**Solution**: Check if app is running on correct port
```python
# Render automatically sets PORT environment variable
# Your app.py should use it:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### Issue: Free Tier Sleeps After 15 Minutes
**Solution**: This is normal for free tier
- First request after sleep takes 30-60 seconds
- Upgrade to paid plan for always-on service
- Or use a service like UptimeRobot to ping every 14 minutes

---

## 💰 Pricing

### Free Tier Includes:
- ✅ 750 hours/month (enough for 1 service)
- ✅ 512 MB RAM
- ✅ Automatic SSL
- ✅ Custom domains
- ✅ Automatic deploys
- ⚠️ Sleeps after 15 min of inactivity
- ⚠️ Limited to 100 GB bandwidth/month

### Paid Plans Start at $7/month:
- Always-on (no sleep)
- More RAM and CPU
- Priority support
- More bandwidth

---

## 🔐 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` files
- ✅ Use Render's environment variable management
- ✅ Rotate secrets regularly

### 2. Database Security
- ✅ Use Internal Database URL (not External)
- ✅ Enable SSL for database connections
- ✅ Regular backups (automatic on Render)

### 3. API Security
- ✅ Enable rate limiting
- ✅ Use HTTPS only
- ✅ Validate all inputs
- ✅ Keep dependencies updated

---

## 📈 Scaling Your Application

### Horizontal Scaling
1. Go to service settings
2. Increase number of instances
3. Render handles load balancing automatically

### Vertical Scaling
1. Upgrade to higher plan
2. More RAM and CPU
3. Better performance

### Database Scaling
1. Upgrade database plan
2. More storage and connections
3. Better performance

---

## 🎉 Your Backend is Live!

**Production URL**: `https://ecom-backend.onrender.com`

**API Endpoints**:
- Health Check: `GET /api/health`
- Books: `GET /api/books`
- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`
- Cart: `GET /api/cart`
- Orders: `POST /api/orders`
- Test Errors: `GET /api/test/error/{type}`

**Next Steps**:
1. ✅ Update frontend with production API URL
2. ✅ Deploy frontend to Vercel/Netlify
3. ✅ Test all features end-to-end
4. ✅ Monitor AIRA dashboard for errors
5. ✅ Set up custom domain (optional)

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **GitHub Issues**: https://github.com/Tuxhar01/Ecom/issues

---

**Deployment Complete!** 🎊

Your e-commerce backend is now running on Render with:
- ✅ PostgreSQL database
- ✅ Automatic HTTPS
- ✅ AIRA error monitoring
- ✅ Continuous deployment from GitHub
- ✅ Free hosting (with limitations)
