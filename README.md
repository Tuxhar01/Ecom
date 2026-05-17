# 📚 Bookstore E-Commerce Platform with AIRA Integration

A full-stack e-commerce web application demonstrating **AIRA error monitoring integration** with a Python Flask backend and React TypeScript frontend.

## 🎯 Project Purpose

This project serves as a **proof-of-concept demonstration** of AIRA's error monitoring capabilities in a realistic e-commerce context. It showcases:

- ✅ Automatic error capture and reporting
- ✅ Intelligent severity classification (P0/P1/P2)
- ✅ Rich contextual information for debugging
- ✅ Multiple error scenarios for testing
- ✅ Real-world application architecture

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  React Frontend │────────▶│  Flask Backend  │────────▶│  SQLite DB      │
│  (TypeScript)   │         │  (Python)       │         │                 │
│                 │         │                 │         │                 │
└─────────────────┘         └────────┬────────┘         └─────────────────┘
                                     │
                                     │ Error Logs
                                     ▼
                            ┌─────────────────┐
                            │                 │
                            │  AIRA Platform  │
                            │  (Webhook)      │
                            │                 │
                            └─────────────────┘
```

---

## ✨ Features

### E-Commerce Functionality
- 🔐 User authentication (JWT-based)
- 📖 Book catalog with search and filters
- 🛒 Shopping cart management
- 💳 Order processing with payment simulation
- 📜 Order history tracking
- 👤 User profile management

### AIRA Integration
- 🚨 Automatic error capture for all exceptions
- 📊 Severity classification (P0/P1/P2)
- 🔍 Rich contextual information (user, request, stack trace)
- 🧪 Test endpoints for each error scenario
- 🔒 Sensitive data sanitization
- ⚡ Non-blocking async webhook calls
- 🔄 Retry logic with exponential backoff

---

## 🛠️ Technology Stack

### Backend
- **Python 3.10+**
- **Flask 3.0+** - Web framework
- **SQLAlchemy 2.0+** - ORM
- **Flask-JWT-Extended** - Authentication
- **Flask-CORS** - Cross-origin support
- **Requests** - HTTP client for AIRA

### Frontend
- **React 18+** - UI library
- **TypeScript 5+** - Type safety
- **Vite** - Build tool
- **Tailwind CSS 3+** - Styling
- **React Router 6+** - Navigation
- **Axios** - HTTP client

### Database
- **SQLite** - Lightweight database for demo

---

## 📁 Project Structure

```
bookstore/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration
│   ├── models.py                 # Database models
│   ├── auth.py                   # JWT utilities
│   ├── aira_handler.py           # AIRA integration ⭐
│   ├── database.py               # DB initialization
│   ├── seed_data.py              # Sample data
│   ├── routes/
│   │   ├── auth_routes.py        # Authentication
│   │   ├── book_routes.py        # Book management
│   │   ├── cart_routes.py        # Cart operations
│   │   ├── order_routes.py       # Order processing
│   │   └── test_routes.py        # Error testing ⭐
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/           # Reusable components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   ├── types/                # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── README.md                      # This file
├── IMPLEMENTATION_PLAN.md        # Detailed plan
├── AIRA_TECHNICAL_SPEC.md        # AIRA integration details
└── TESTING_GUIDE.md              # Error testing guide
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn
- AIRA webhook URL and API key

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd bookstore

# Or if starting fresh in current directory
# Files will be created in current workspace
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your AIRA credentials

# Initialize database and seed data
python seed_data.py

# Start the Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will run on `http://localhost:5173`

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-here-change-in-production
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///bookstore.db

# AIRA Integration (⭐ REQUIRED)
AIRA_WEBHOOK_URL=https://your-aira-instance.com/webhook
AIRA_API_KEY=aira_your_api_key_here

# CORS
FRONTEND_URL=http://localhost:5173

# Optional AIRA Settings
AIRA_ENABLED=true
AIRA_LOG_LEVEL=ERROR
AIRA_MAX_RETRIES=3
AIRA_TIMEOUT=5
```

**Important**: Replace `AIRA_WEBHOOK_URL` and `AIRA_API_KEY` with your actual AIRA credentials.

---

## 🧪 Testing AIRA Integration

### Test User Credentials

The application comes with pre-seeded test users:

- **Regular User**: `user@example.com` / `password123`
- **Admin User**: `admin@example.com` / `admin123`
- **Test User**: `test@example.com` / `test123`

### Error Testing Endpoints

The application includes dedicated endpoints to trigger different error scenarios:

| Endpoint | Method | Severity | Description |
|----------|--------|----------|-------------|
| `/api/test/error/database` | GET | P0 | Database connection failure |
| `/api/test/error/payment` | POST | P1 | Payment processing error |
| `/api/test/error/auth` | GET | P1 | Authentication failure |
| `/api/test/error/stock` | POST | P2 | Insufficient stock error |
| `/api/test/error/validation` | POST | P2 | Validation error |
| `/api/books/99999` | GET | P2 | Invalid product ID |

### Testing Steps

1. **Start both backend and frontend servers**

2. **Test Database Error (P0)**
   ```bash
   curl http://localhost:5000/api/test/error/database
   ```

3. **Test Payment Error (P1)** - Requires authentication
   ```bash
   # First, login to get token
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"password123"}'
   
   # Use the token from response
   curl -X POST http://localhost:5000/api/test/error/payment \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"amount": 100.00}'
   ```

4. **Test Invalid Book ID (P2)**
   ```bash
   curl http://localhost:5000/api/books/99999
   ```

5. **Check AIRA Dashboard**
   - Verify errors appear in your AIRA instance
   - Check severity levels are correct
   - Confirm context information is included
   - Review stack traces

### Expected AIRA Payload

Each error will send a payload like this to AIRA:

```json
{
  "message": "Payment processing failed for order #12345",
  "stack_trace": "Traceback (most recent call last):\n  File...",
  "severity": "P1",
  "timestamp": "2026-05-17T08:49:37.265Z",
  "context": {
    "user_id": "user_123",
    "user_email": "user@example.com",
    "endpoint": "api.create_order",
    "method": "POST",
    "path": "/api/orders",
    "remote_addr": "127.0.0.1",
    "user_agent": "Mozilla/5.0...",
    "error_type": "PaymentError",
    "module": "order_routes",
    "function": "create_order",
    "line_number": 45
  }
}
```

---

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe"
  }
}
```

### Book Endpoints

#### List Books
```http
GET /api/books?page=1&per_page=10&search=python

Response:
{
  "books": [...],
  "total": 20,
  "page": 1,
  "per_page": 10
}
```

#### Get Book Details
```http
GET /api/books/1

Response:
{
  "id": 1,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "price": 29.99,
  "stock": 15,
  "description": "...",
  "cover_image": "..."
}
```

### Cart Endpoints (Protected)

#### Get Cart
```http
GET /api/cart
Authorization: Bearer YOUR_TOKEN

Response:
{
  "items": [
    {
      "id": 1,
      "book": {...},
      "quantity": 2
    }
  ],
  "total": 59.98
}
```

#### Add to Cart
```http
POST /api/cart
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "book_id": 1,
  "quantity": 2
}
```

### Order Endpoints (Protected)

#### Create Order
```http
POST /api/orders
Authorization: Bearer YOUR_TOKEN

Response:
{
  "order_id": 123,
  "total_amount": 59.98,
  "status": "pending",
  "items": [...]
}
```

#### Get Order History
```http
GET /api/orders
Authorization: Bearer YOUR_TOKEN

Response:
{
  "orders": [...]
}
```

---

## 🔒 Security Features

- ✅ Password hashing with Werkzeug
- ✅ JWT token-based authentication
- ✅ CORS protection
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Sensitive data redaction in logs
- ✅ Rate limiting on API endpoints

---

## 📊 Database Schema

### Users
- `id` (Primary Key)
- `email` (Unique)
- `username` (Unique)
- `password_hash`
- `created_at`

### Books
- `id` (Primary Key)
- `title`
- `author`
- `price`
- `stock`
- `description`
- `cover_image`
- `isbn` (Unique)
- `created_at`

### Orders
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `total_amount`
- `status`
- `created_at`

### OrderItems
- `id` (Primary Key)
- `order_id` (Foreign Key)
- `book_id` (Foreign Key)
- `quantity`
- `price`

### Cart
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `book_id` (Foreign Key)
- `quantity`
- `created_at`

---

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Issue**: Database errors
```bash
# Reinitialize database
rm bookstore.db
python seed_data.py
```

**Issue**: AIRA errors not appearing
- Check `AIRA_WEBHOOK_URL` is correct
- Verify `AIRA_API_KEY` is valid
- Check network connectivity
- Review backend logs for AIRA handler errors

### Frontend Issues

**Issue**: `Cannot connect to backend`
- Ensure backend is running on port 5000
- Check CORS configuration in backend
- Verify `FRONTEND_URL` in `.env`

**Issue**: Build errors
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📖 Additional Documentation

- **[IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)** - Detailed implementation plan and architecture
- **[AIRA_TECHNICAL_SPEC.md](./AIRA_TECHNICAL_SPEC.md)** - AIRA integration technical specifications
- **[TESTING_GUIDE.md](./TESTING_GUIDE.md)** - Comprehensive testing guide for error scenarios

---

## 🎓 Learning Resources

### AIRA Integration
- Understanding error severity levels
- Best practices for error logging
- Context enrichment strategies
- Webhook retry mechanisms

### Flask Development
- RESTful API design
- JWT authentication
- SQLAlchemy ORM
- Error handling patterns

### React + TypeScript
- Component architecture
- State management
- API integration
- Type safety

---

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**
   - Use strong, unique secrets
   - Never commit `.env` to version control
   - Use environment-specific configurations

2. **Database**
   - Migrate to PostgreSQL or MySQL for production
   - Set up proper backups
   - Use connection pooling

3. **Security**
   - Enable HTTPS
   - Set up proper CORS policies
   - Implement rate limiting
   - Add request validation

4. **AIRA**
   - Monitor webhook success rate
   - Set up alerts for AIRA failures
   - Review error patterns regularly

---

## 🤝 Contributing

This is a demonstration project. For improvements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📝 License

This project is created for demonstration purposes.

---

## 📞 Support

For questions about:
- **AIRA Integration**: Check [AIRA_TECHNICAL_SPEC.md](./AIRA_TECHNICAL_SPEC.md)
- **Error Testing**: See [TESTING_GUIDE.md](./TESTING_GUIDE.md)
- **Implementation**: Review [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)

---

## ✅ Project Status

- [x] Backend API implementation
- [x] AIRA integration
- [x] Database models and migrations
- [x] Authentication system
- [x] Frontend React application
- [x] Error testing endpoints
- [x] Documentation
- [ ] Docker containerization (optional)
- [ ] CI/CD pipeline (optional)

---

**Built with ❤️ to demonstrate AIRA error monitoring capabilities**