# 🚀 Deployment Plan - E-Commerce Platform with AIRA Integration

Complete guide for deploying the bookstore application to production.

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Database Migration](#database-migration)
6. [AIRA Configuration](#aira-configuration)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Rollback Plan](#rollback-plan)

---

## ✅ Pre-Deployment Checklist

### Code Preparation
- [ ] All code committed to Git
- [ ] `.env` files excluded from repository
- [ ] `.env.example` files included
- [ ] Dependencies documented in requirements.txt / package.json
- [ ] Database migrations tested
- [ ] All tests passing
- [ ] Security audit completed

### Infrastructure
- [ ] Production server provisioned
- [ ] Domain name configured
- [ ] SSL certificate obtained
- [ ] Database server ready
- [ ] AIRA webhook accessible
- [ ] Backup strategy in place

### Configuration
- [ ] Production environment variables prepared
- [ ] AIRA credentials verified
- [ ] Database credentials secured
- [ ] JWT secrets generated
- [ ] CORS origins configured

---

## 🌍 Environment Setup

### Recommended Hosting Options

#### Backend Options
1. **Heroku** (Easiest)
   - Free tier available
   - Built-in PostgreSQL
   - Easy deployment

2. **AWS EC2** (Flexible)
   - Full control
   - Scalable
   - Requires more setup

3. **DigitalOcean** (Balanced)
   - Simple droplets
   - Good pricing
   - Easy to manage

4. **Railway** (Modern)
   - Git-based deployment
   - Free tier
   - Simple setup

#### Frontend Options
1. **Vercel** (Recommended)
   - Free tier
   - Automatic deployments
   - CDN included

2. **Netlify**
   - Free tier
   - Easy setup
   - Good performance

3. **AWS S3 + CloudFront**
   - Highly scalable
   - Low cost
   - More complex

---

## 🔧 Backend Deployment

### Option 1: Heroku Deployment

#### 1. Install Heroku CLI
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Create Heroku App
```bash
cd backend
heroku login
heroku create your-bookstore-api
```

#### 3. Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

#### 4. Set Environment Variables
```bash
heroku config:set FLASK_SECRET_KEY="your-production-secret"
heroku config:set JWT_SECRET_KEY="your-jwt-secret"
heroku config:set AIRA_WEBHOOK_URL="your-aira-webhook"
heroku config:set AIRA_API_KEY="your-aira-key"
heroku config:set FRONTEND_URL="https://your-frontend.vercel.app"
```

#### 5. Create Procfile
```bash
# backend/Procfile
web: gunicorn app:app
```

#### 6. Add gunicorn to requirements.txt
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

#### 7. Deploy
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

#### 8. Initialize Database
```bash
heroku run python seed_data.py
```

### Option 2: AWS EC2 Deployment

#### 1. Launch EC2 Instance
- Ubuntu 22.04 LTS
- t2.micro (free tier)
- Security group: Allow ports 22, 80, 443

#### 2. Connect and Setup
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3-pip python3-venv -y

# Install Nginx
sudo apt install nginx -y

# Install Supervisor
sudo apt install supervisor -y
```

#### 3. Deploy Application
```bash
# Clone repository
git clone https://github.com/Tuxhar01/Ecom.git
cd Ecom/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create .env file
nano .env
# Add production environment variables
```

#### 4. Configure Gunicorn
```bash
# Create gunicorn config
nano gunicorn_config.py
```

```python
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
```

#### 5. Configure Supervisor
```bash
sudo nano /etc/supervisor/conf.d/bookstore.conf
```

```ini
[program:bookstore]
directory=/home/ubuntu/Ecom/backend
command=/home/ubuntu/Ecom/backend/venv/bin/gunicorn -c gunicorn_config.py app:app
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/bookstore/err.log
stdout_logfile=/var/log/bookstore/out.log
```

#### 6. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/bookstore
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/bookstore /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start application
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start bookstore
```

#### 7. Setup SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Option 3: Railway Deployment

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

#### 2. Login and Deploy
```bash
cd backend
railway login
railway init
railway up
```

#### 3. Add Environment Variables
```bash
railway variables set FLASK_SECRET_KEY="your-secret"
railway variables set JWT_SECRET_KEY="your-jwt-secret"
railway variables set AIRA_WEBHOOK_URL="your-aira-webhook"
railway variables set AIRA_API_KEY="your-aira-key"
```

---

## 🎨 Frontend Deployment

### Option 1: Vercel Deployment (Recommended)

#### 1. Install Vercel CLI
```bash
npm install -g vercel
```

#### 2. Deploy
```bash
cd frontend
vercel login
vercel
```

#### 3. Configure Environment
Create `vercel.json`:
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend-url.com/api/:path*"
    }
  ]
}
```

#### 4. Set Environment Variables
```bash
vercel env add VITE_API_URL production
# Enter: https://your-backend-url.com
```

### Option 2: Netlify Deployment

#### 1. Install Netlify CLI
```bash
npm install -g netlify-cli
```

#### 2. Build and Deploy
```bash
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

#### 3. Configure Redirects
Create `frontend/public/_redirects`:
```
/api/*  https://your-backend-url.com/api/:splat  200
/*  /index.html  200
```

### Option 3: AWS S3 + CloudFront

#### 1. Build Frontend
```bash
cd frontend
npm run build
```

#### 2. Create S3 Bucket
```bash
aws s3 mb s3://your-bookstore-frontend
aws s3 website s3://your-bookstore-frontend --index-document index.html
```

#### 3. Upload Files
```bash
aws s3 sync dist/ s3://your-bookstore-frontend --acl public-read
```

#### 4. Create CloudFront Distribution
- Origin: S3 bucket
- Default root object: index.html
- Enable HTTPS

---

## 🗄️ Database Migration

### From SQLite to PostgreSQL

#### 1. Export Data
```python
# export_data.py
from models import User, Book, db_session
import json

users = [u.to_dict() for u in db_session.query(User).all()]
books = [b.to_dict() for b in db_session.query(Book).all()]

with open('users.json', 'w') as f:
    json.dump(users, f)

with open('books.json', 'w') as f:
    json.dump(books, f)
```

#### 2. Update Database URL
```python
# config.py
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:pass@localhost/bookstore')
```

#### 3. Install PostgreSQL Driver
```bash
pip install psycopg2-binary
```

#### 4. Import Data
```python
# import_data.py
import json
from models import User, Book, db_session, init_db

init_db()

with open('users.json') as f:
    users = json.load(f)
    for user_data in users:
        user = User(**user_data)
        db_session.add(user)

with open('books.json') as f:
    books = json.load(f)
    for book_data in books:
        book = Book(**book_data)
        db_session.add(book)

db_session.commit()
```

---

## 🔍 AIRA Configuration

### Production Setup

#### 1. Verify AIRA Webhook
```bash
curl -X POST https://your-aira-instance.com/webhook \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"test": "message"}'
```

#### 2. Update Environment Variables
```bash
# Production .env
AIRA_WEBHOOK_URL=https://your-production-aira.com/webhook
AIRA_API_KEY=your-production-api-key
AIRA_ENABLED=true
AIRA_LOG_LEVEL=ERROR
```

#### 3. Test Error Logging
```bash
curl https://your-api.com/api/test/error/database
```

#### 4. Monitor AIRA Dashboard
- Check error appears
- Verify context is complete
- Confirm severity is correct

---

## 📊 Monitoring & Maintenance

### Application Monitoring

#### 1. Setup Health Checks
```python
# Add to app.py
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })
```

#### 2. Configure Uptime Monitoring
- Use UptimeRobot or Pingdom
- Monitor `/health` endpoint
- Alert on downtime

#### 3. Log Aggregation
- Use Papertrail or Loggly
- Centralize logs
- Set up alerts

### Database Maintenance

#### 1. Automated Backups
```bash
# Heroku
heroku pg:backups:schedule DATABASE_URL --at '02:00 America/Los_Angeles'

# AWS RDS
# Enable automated backups in console
```

#### 2. Regular Maintenance
```sql
-- PostgreSQL
VACUUM ANALYZE;
REINDEX DATABASE bookstore;
```

### Security Updates

#### 1. Dependency Updates
```bash
# Backend
pip list --outdated
pip install --upgrade package-name

# Frontend
npm outdated
npm update
```

#### 2. Security Scanning
```bash
# Python
pip install safety
safety check

# Node.js
npm audit
npm audit fix
```

---

## 🔄 Rollback Plan

### Quick Rollback Steps

#### 1. Heroku Rollback
```bash
heroku releases
heroku rollback v123
```

#### 2. Vercel Rollback
```bash
vercel rollback
```

#### 3. Manual Rollback
```bash
# Checkout previous version
git checkout previous-tag
git push heroku main --force
```

### Database Rollback

#### 1. Restore from Backup
```bash
# Heroku
heroku pg:backups:restore b001 DATABASE_URL

# PostgreSQL
pg_restore -d bookstore backup.dump
```

---

## 🎯 Post-Deployment Checklist

### Verification
- [ ] Backend API accessible
- [ ] Frontend loads correctly
- [ ] Database connected
- [ ] AIRA logging works
- [ ] Authentication functional
- [ ] All endpoints responding
- [ ] SSL certificate valid
- [ ] CORS configured correctly

### Performance
- [ ] Response times acceptable
- [ ] No memory leaks
- [ ] Database queries optimized
- [ ] CDN configured
- [ ] Caching enabled

### Security
- [ ] Environment variables secured
- [ ] Database credentials rotated
- [ ] API keys protected
- [ ] HTTPS enforced
- [ ] Rate limiting active

### Monitoring
- [ ] Health checks configured
- [ ] Error tracking active
- [ ] Uptime monitoring setup
- [ ] Log aggregation working
- [ ] Backup schedule verified

---

## 📝 Environment Variables Reference

### Backend (.env)
```bash
# Flask
FLASK_SECRET_KEY=<strong-random-string>
JWT_SECRET_KEY=<strong-random-string>
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# AIRA
AIRA_WEBHOOK_URL=https://your-aira.com/webhook
AIRA_API_KEY=aira_your_key
AIRA_ENABLED=true
AIRA_LOG_LEVEL=ERROR

# CORS
FRONTEND_URL=https://your-frontend.vercel.app
```

### Frontend (.env)
```bash
VITE_API_URL=https://your-backend.herokuapp.com
```

---

## 🆘 Troubleshooting

### Common Issues

#### Backend Not Starting
```bash
# Check logs
heroku logs --tail

# Verify environment variables
heroku config

# Check database connection
heroku pg:info
```

#### AIRA Not Logging
```bash
# Test webhook
curl -X POST $AIRA_WEBHOOK_URL \
  -H "X-API-Key: $AIRA_API_KEY" \
  -d '{"test": "message"}'

# Check backend logs
heroku logs --tail | grep AIRA
```

#### CORS Errors
```python
# Update CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend.vercel.app"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 📞 Support Contacts

- **Backend Issues**: Check Heroku/Railway logs
- **Frontend Issues**: Check Vercel/Netlify logs
- **AIRA Issues**: Contact AIRA support
- **Database Issues**: Check database provider logs

---

## 🎉 Deployment Complete!

Once deployed, your application will be:
- ✅ Accessible globally
- ✅ Secured with HTTPS
- ✅ Monitored by AIRA
- ✅ Backed up regularly
- ✅ Scalable and reliable

**Production URLs:**
- Backend: `https://your-api.herokuapp.com`
- Frontend: `https://your-app.vercel.app`
- AIRA Dashboard: `https://your-aira-instance.com`

---

**Last Updated**: 2026-05-17
**Version**: 1.0.0