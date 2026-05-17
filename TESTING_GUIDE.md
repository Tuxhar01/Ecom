# 🧪 AIRA Error Testing Guide

This guide provides step-by-step instructions for testing all AIRA error monitoring scenarios in the bookstore application.

---

## 📋 Prerequisites

Before testing, ensure:

- ✅ Backend server is running (`python app.py`)
- ✅ Frontend server is running (`npm run dev`)
- ✅ AIRA webhook URL is configured in `.env`
- ✅ AIRA API key is set in `.env`
- ✅ Database is seeded with sample data
- ✅ You have access to AIRA dashboard

---

## 🎯 Testing Overview

We will test **6 different error scenarios** covering all severity levels:

| # | Scenario | Severity | Endpoint | Auth Required |
|---|----------|----------|----------|---------------|
| 1 | Database Connection Failure | P0 | `/api/test/error/database` | No |
| 2 | Payment Processing Error | P1 | `/api/test/error/payment` | Yes |
| 3 | Authentication Failure | P1 | `/api/test/error/auth` | No |
| 4 | Stock Validation Error | P2 | `/api/test/error/stock` | Yes |
| 5 | Invalid Product ID | P2 | `/api/books/99999` | No |
| 6 | Validation Error | P2 | `/api/test/error/validation` | No |

---

## 🔧 Setup for Testing

### 1. Get Authentication Token

Most error scenarios require authentication. First, obtain a JWT token:

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Using Frontend:**
1. Navigate to `http://localhost:5173`
2. Click "Login"
3. Enter credentials: `user@example.com` / `password123`
4. Open browser DevTools → Network tab
5. Look for the `access_token` in the login response

**Save the token** - you'll need it for authenticated requests.

---

## 🚨 Test Scenario 1: Database Connection Failure (P0)

### Description
Simulates a critical database connection failure - the most severe type of error.

### Expected Behavior
- HTTP Status: `500 Internal Server Error`
- AIRA Severity: `P0`
- Error Type: `DatabaseError`

### Test Steps

**Using cURL:**
```bash
curl -v http://localhost:5000/api/test/error/database
```

**Using Frontend:**
1. Open browser console
2. Run:
```javascript
fetch('http://localhost:5000/api/test/error/database')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

**Using Postman:**
- Method: `GET`
- URL: `http://localhost:5000/api/test/error/database`
- Click "Send"

### Expected Response
```json
{
  "error": "Database connection failed",
  "severity": "P0",
  "message": "Critical database error occurred"
}
```

### Verify in AIRA
Check your AIRA dashboard for:
- ✅ Error message: "Database connection failed"
- ✅ Severity: P0
- ✅ Stack trace included
- ✅ Context: endpoint, method, path
- ✅ Timestamp in ISO format

---

## 💳 Test Scenario 2: Payment Processing Error (P1)

### Description
Simulates a payment gateway failure during checkout.

### Expected Behavior
- HTTP Status: `402 Payment Required`
- AIRA Severity: `P1`
- Error Type: `PaymentError`

### Test Steps

**Using cURL:**
```bash
# Replace YOUR_TOKEN with actual token from login
curl -X POST http://localhost:5000/api/test/error/payment \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 99.99,
    "payment_method": "credit_card"
  }'
```

**Using Frontend:**
1. Login first
2. Open browser console
3. Run:
```javascript
fetch('http://localhost:5000/api/test/error/payment', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    amount: 99.99,
    payment_method: 'credit_card'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Expected Response
```json
{
  "error": "Payment processing failed",
  "severity": "P1",
  "message": "Payment gateway timeout for amount $99.99"
}
```

### Verify in AIRA
Check for:
- ✅ Error message: "Payment processing failed"
- ✅ Severity: P1
- ✅ User context: user_id, user_email
- ✅ Request data: amount, payment_method
- ✅ Stack trace with PaymentError

---

## 🔐 Test Scenario 3: Authentication Failure (P1)

### Description
Simulates an authentication/authorization failure.

### Expected Behavior
- HTTP Status: `401 Unauthorized`
- AIRA Severity: `P1`
- Error Type: `AuthenticationError`

### Test Steps

**Using cURL:**
```bash
curl -v http://localhost:5000/api/test/error/auth
```

**Using Frontend:**
```javascript
fetch('http://localhost:5000/api/test/error/auth')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Expected Response
```json
{
  "error": "Authentication failed",
  "severity": "P1",
  "message": "Invalid or expired JWT token"
}
```

### Verify in AIRA
Check for:
- ✅ Error message: "Authentication failed"
- ✅ Severity: P1
- ✅ Context: attempted endpoint
- ✅ User: anonymous (no auth)

---

## 📦 Test Scenario 4: Stock Validation Error (P2)

### Description
Simulates attempting to order more items than available in stock.

### Expected Behavior
- HTTP Status: `400 Bad Request`
- AIRA Severity: `P2`
- Error Type: `StockError`

### Test Steps

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/test/error/stock \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "quantity": 1000
  }'
```

**Using Frontend:**
```javascript
fetch('http://localhost:5000/api/test/error/stock', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    book_id: 1,
    quantity: 1000
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Expected Response
```json
{
  "error": "Insufficient stock",
  "severity": "P2",
  "message": "Insufficient stock for book 'Clean Code'. Requested: 1000, Available: 15"
}
```

### Verify in AIRA
Check for:
- ✅ Error message: "Stock validation failed"
- ✅ Severity: P2
- ✅ Context: book_id, requested quantity, available stock
- ✅ User information included

---

## 🔍 Test Scenario 5: Invalid Product ID (P2)

### Description
Attempts to access a non-existent book.

### Expected Behavior
- HTTP Status: `404 Not Found`
- AIRA Severity: `P2`
- Error Type: `ValueError`

### Test Steps

**Using cURL:**
```bash
curl -v http://localhost:5000/api/books/99999
```

**Using Frontend:**
1. Navigate to: `http://localhost:5173/books/99999`
2. Or use console:
```javascript
fetch('http://localhost:5000/api/books/99999')
  .then(res => res.json())
  .then(data => console.log(data));
```

### Expected Response
```json
{
  "error": "Book not found",
  "severity": "P2",
  "message": "Book with ID 99999 not found"
}
```

### Verify in AIRA
Check for:
- ✅ Error message: "Invalid book ID requested"
- ✅ Severity: P2
- ✅ Context: requested book_id (99999)
- ✅ Request path: /api/books/99999

---

## ✅ Test Scenario 6: Validation Error (P2)

### Description
Simulates input validation failure.

### Expected Behavior
- HTTP Status: `400 Bad Request`
- AIRA Severity: `P2`
- Error Type: `ValidationError`

### Test Steps

**Using cURL:**
```bash
curl -X POST http://localhost:5000/api/test/error/validation \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid-email",
    "quantity": -5
  }'
```

**Using Frontend:**
```javascript
fetch('http://localhost:5000/api/test/error/validation', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'invalid-email',
    quantity: -5
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Expected Response
```json
{
  "error": "Validation failed",
  "severity": "P2",
  "message": "Invalid input data",
  "details": {
    "email": "Invalid email format",
    "quantity": "Must be positive"
  }
}
```

### Verify in AIRA
Check for:
- ✅ Error message: "Validation failed"
- ✅ Severity: P2
- ✅ Context: validation errors
- ✅ Request body (sanitized)

---

## 🔄 Testing Real User Flows

### Flow 1: Complete Purchase with Error

1. **Login**
   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"password123"}'
   ```

2. **Add Book to Cart**
   ```bash
   curl -X POST http://localhost:5000/api/cart \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"book_id": 1, "quantity": 2}'
   ```

3. **Attempt Checkout (triggers payment error)**
   ```bash
   curl -X POST http://localhost:5000/api/orders \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

### Flow 2: Browse and Trigger Errors

1. **Browse Books**
   ```bash
   curl http://localhost:5000/api/books
   ```

2. **Try Invalid Book**
   ```bash
   curl http://localhost:5000/api/books/99999
   ```

3. **Try Excessive Quantity**
   ```bash
   curl -X POST http://localhost:5000/api/cart \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"book_id": 1, "quantity": 1000}'
   ```

---

## 📊 AIRA Dashboard Verification

After running tests, verify in AIRA dashboard:

### 1. Error Count
- Should see 6+ errors (one for each test)
- Errors should be timestamped correctly

### 2. Severity Distribution
- **P0**: 1 error (database)
- **P1**: 2 errors (payment, auth)
- **P2**: 3 errors (stock, invalid ID, validation)

### 3. Context Information
Each error should include:
- ✅ Clear error message
- ✅ Full stack trace
- ✅ Request method (GET/POST)
- ✅ Request path
- ✅ User information (if authenticated)
- ✅ Timestamp in ISO format
- ✅ Error type/class

### 4. Stack Traces
Verify stack traces show:
- File names
- Line numbers
- Function names
- Full traceback

---

## 🐛 Troubleshooting

### Issue: Errors not appearing in AIRA

**Check:**
1. AIRA webhook URL is correct in `.env`
2. AIRA API key is valid
3. Backend logs for AIRA handler errors
4. Network connectivity to AIRA

**Debug:**
```bash
# Check backend logs
tail -f backend/logs/app.log

# Test AIRA connection
curl -X POST YOUR_AIRA_WEBHOOK_URL \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"test": "message"}'
```

### Issue: Authentication errors

**Solution:**
1. Ensure you're using a fresh token
2. Token expires after 24 hours - login again
3. Check Authorization header format: `Bearer TOKEN`

### Issue: 404 errors on test endpoints

**Check:**
1. Backend server is running
2. Using correct port (5000)
3. Endpoint path is correct
4. Flask app loaded test routes

---

## 📝 Test Checklist

Use this checklist to track your testing:

- [ ] Backend server running
- [ ] Frontend server running
- [ ] AIRA configured in `.env`
- [ ] Obtained authentication token
- [ ] Test 1: Database error (P0) ✓
- [ ] Test 2: Payment error (P1) ✓
- [ ] Test 3: Auth error (P1) ✓
- [ ] Test 4: Stock error (P2) ✓
- [ ] Test 5: Invalid ID (P2) ✓
- [ ] Test 6: Validation error (P2) ✓
- [ ] Verified all errors in AIRA dashboard
- [ ] Checked severity levels are correct
- [ ] Confirmed context information is complete
- [ ] Reviewed stack traces

---

## 🎯 Advanced Testing

### Rate Limiting Test

Trigger multiple errors rapidly to test rate limiting:

```bash
# Run this script to send 10 requests quickly
for i in {1..10}; do
  curl http://localhost:5000/api/books/99999 &
done
wait
```

**Expected**: Only some errors sent to AIRA (rate limited)

### Concurrent Error Test

Test multiple error types simultaneously:

```bash
# Terminal 1
curl http://localhost:5000/api/test/error/database

# Terminal 2 (at same time)
curl http://localhost:5000/api/books/99999

# Terminal 3 (at same time)
curl http://localhost:5000/api/test/error/auth
```

**Expected**: All errors captured and sent to AIRA

---

## 📈 Performance Testing

### Response Time Test

Measure impact of AIRA logging on response time:

```bash
# Without error (baseline)
time curl http://localhost:5000/api/books

# With error (AIRA overhead)
time curl http://localhost:5000/api/books/99999
```

**Expected**: Minimal overhead (<50ms) due to async webhook calls

---

## 🎓 Learning Outcomes

After completing this testing guide, you should understand:

1. ✅ How AIRA captures different error severities
2. ✅ What contextual information is included
3. ✅ How to trigger and test error scenarios
4. ✅ How to verify errors in AIRA dashboard
5. ✅ Best practices for error monitoring

---

## 📞 Next Steps

1. **Review AIRA Dashboard**: Analyze error patterns
2. **Test Custom Scenarios**: Create your own error cases
3. **Monitor Production**: Apply learnings to real applications
4. **Optimize**: Adjust severity levels and context as needed

---

## 📚 Additional Resources

- [AIRA_TECHNICAL_SPEC.md](./AIRA_TECHNICAL_SPEC.md) - Technical implementation details
- [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) - Overall project architecture
- [README.md](./README.md) - Project overview and setup

---

**Happy Testing! 🚀**