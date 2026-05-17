# 🔧 Backend - Bookstore API with AIRA Integration

Python Flask backend with comprehensive AIRA error monitoring integration.

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your AIRA credentials:
# AIRA_WEBHOOK_URL=https://your-aira-instance.com/webhook
# AIRA_API_KEY=aira_your_api_key_here
```

### 4. Initialize Database

```bash
python seed_data.py
```

This will create the database and populate it with:
- 20 sample books
- 3 test users

### 5. Run the Server

```bash
python app.py
```

Server will start at: `http://localhost:5000`

## 📚 Test Users

| Email | Password | Role |
|-------|----------|------|
| user@example.com | password123 | Regular User |
| admin@example.com | admin123 | Admin |
| test@example.com | test123 | Test User |

## 🧪 Testing AIRA Integration

### Test Endpoints

All test endpoints are under `/api/test/error/`:

1. **Database Error (P0)**
   ```bash
   curl http://localhost:5000/api/test/error/database
   ```

2. **Payment Error (P1)** - Requires authentication
   ```bash
   # First login to get token
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d "{\"email\":\"user@example.com\",\"password\":\"password123\"}"
   
   # Then test payment error
   curl -X POST http://localhost:5000/api/test/error/payment \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"amount\": 99.99}"
   ```

3. **Auth Error (P1)**
   ```bash
   curl http://localhost:5000/api/test/error/auth
   ```

4. **Stock Error (P2)** - Requires authentication
   ```bash
   curl -X POST http://localhost:5000/api/test/error/stock \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"book_id\": 1, \"quantity\": 1000}"
   ```

5. **Validation Error (P2)**
   ```bash
   curl -X POST http://localhost:5000/api/test/error/validation \
     -H "Content-Type: application/json" \
     -d "{\"email\": \"invalid\", \"quantity\": -5}"
   ```

6. **Invalid Book ID (P2)**
   ```bash
   curl http://localhost:5000/api/books/99999
   ```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user (protected)

### Books
- `GET /api/books` - List all books (with pagination & search)
- `GET /api/books/<id>` - Get book details
- `POST /api/books` - Create book (protected)
- `PUT /api/books/<id>` - Update book (protected)
- `DELETE /api/books/<id>` - Delete book (protected)

### Cart
- `GET /api/cart` - Get user's cart (protected)
- `POST /api/cart` - Add item to cart (protected)
- `PUT /api/cart/<id>` - Update cart item (protected)
- `DELETE /api/cart/<id>` - Remove from cart (protected)
- `DELETE /api/cart` - Clear cart (protected)

### Orders
- `GET /api/orders` - Get user's orders (protected)
- `GET /api/orders/<id>` - Get order details (protected)
- `POST /api/orders` - Create order from cart (protected)

### Testing
- `GET /api/test/error/database` - Test P0 error
- `POST /api/test/error/payment` - Test P1 error (protected)
- `GET /api/test/error/auth` - Test P1 error
- `POST /api/test/error/stock` - Test P2 error (protected)
- `POST /api/test/error/validation` - Test P2 error
- `GET /api/test/health` - Health check

## 🔍 Verify AIRA Integration

After triggering errors, check your AIRA dashboard for:
- ✅ Error messages
- ✅ Severity levels (P0/P1/P2)
- ✅ Stack traces
- ✅ Context information (user, request, etc.)
- ✅ Timestamps

## 📁 Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py              # Configuration
├── models.py              # Database models
├── auth.py                # JWT authentication
├── aira_handler.py        # AIRA integration ⭐
├── seed_data.py           # Database seeding
├── routes/
│   ├── auth_routes.py     # Authentication endpoints
│   ├── book_routes.py     # Book management
│   ├── cart_routes.py     # Cart operations
│   ├── order_routes.py    # Order processing
│   └── test_routes.py     # Error testing ⭐
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
└── .gitignore
```

## 🛠️ Development

### Reset Database

```bash
python seed_data.py
```

This will drop all tables and recreate them with fresh data.

### Check Logs

The application logs all operations. AIRA-related logs will show:
- When errors are sent to AIRA
- If AIRA webhook fails
- Rate limiting information

### Troubleshooting

**Issue**: `ModuleNotFoundError`
```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

**Issue**: Database errors
```bash
# Reset database
python seed_data.py
```

**Issue**: AIRA errors not appearing
- Check `.env` file has correct `AIRA_WEBHOOK_URL` and `AIRA_API_KEY`
- Verify AIRA service is running
- Check backend logs for AIRA handler errors

## 🔒 Security Notes

- JWT tokens expire after 24 hours
- Passwords are hashed using Werkzeug
- Sensitive data is sanitized before sending to AIRA
- CORS is configured for frontend origin only

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| FLASK_SECRET_KEY | Flask session secret | Yes |
| JWT_SECRET_KEY | JWT token secret | Yes |
| DATABASE_URL | Database connection string | Yes |
| AIRA_WEBHOOK_URL | AIRA webhook endpoint | Yes |
| AIRA_API_KEY | AIRA API key | Yes |
| FRONTEND_URL | Frontend origin for CORS | Yes |
| AIRA_ENABLED | Enable/disable AIRA | No (default: true) |
| AIRA_LOG_LEVEL | Minimum log level for AIRA | No (default: ERROR) |
| AIRA_MAX_RETRIES | Webhook retry attempts | No (default: 3) |
| AIRA_TIMEOUT | Webhook timeout in seconds | No (default: 5) |
| AIRA_RATE_LIMIT | Max errors per minute | No (default: 100) |

## 🎯 Next Steps

1. ✅ Backend is complete and ready
2. 🔄 Configure your AIRA credentials in `.env`
3. 🧪 Test all error scenarios
4. 📊 Verify errors appear in AIRA dashboard
5. 🎨 Build the frontend (see `../frontend/`)

---

**Backend Complete! Ready for AIRA testing! 🚀**