# 🎨 Frontend - Bookstore React Application

React + TypeScript frontend with Tailwind CSS for the AIRA-integrated bookstore platform.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will run at: `http://localhost:5173`

## ✨ Features

### User Interface
- 📚 Book catalog with grid layout
- 🛒 Shopping cart management
- 🔐 User authentication (login/register)
- 💳 Checkout process
- 🧪 AIRA error testing buttons

### Functionality
- Browse 20 sample books
- Add books to cart
- Update cart quantities
- Place orders
- Test AIRA error scenarios with one click

## 🧪 Testing AIRA Integration

The frontend includes dedicated buttons to trigger each error scenario:

1. **P0: Database Error** - Critical system failure
2. **P1: Payment Error** - Payment processing failure (requires login)
3. **P1: Auth Error** - Authentication failure
4. **P2: Stock Error** - Insufficient inventory (requires login)
5. **P2: Validation Error** - Invalid input data

Click any button to trigger the error and check your AIRA dashboard!

## 🔑 Test Credentials

Use these credentials to login:

- **Email**: `user@example.com`
- **Password**: `password123`

Or register a new account!

## 📁 Project Structure

```
frontend/
├── src/
│   ├── types/
│   │   └── index.ts          # TypeScript interfaces
│   ├── services/
│   │   └── api.ts            # API client with axios
│   ├── App.tsx               # Main application component
│   ├── main.tsx              # Entry point
│   ├── index.css             # Tailwind CSS imports
│   └── vite-env.d.ts         # Vite types
├── index.html                # HTML template
├── package.json              # Dependencies
├── vite.config.ts            # Vite configuration
├── tsconfig.json             # TypeScript configuration
├── tailwind.config.js        # Tailwind CSS configuration
└── postcss.config.js         # PostCSS configuration
```

## 🛠️ Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🎨 UI Components

### Authentication
- Login form with email/password
- Registration form with email/username/password
- Toggle between login and register
- Test credentials displayed

### Book Catalog
- Grid layout (2 columns on desktop)
- Book cards with:
  - Title and author
  - Description (truncated)
  - Price
  - Stock count
  - Add to cart button

### Shopping Cart
- List of cart items
- Subtotals for each item
- Total amount
- Checkout button
- Empty state message

### AIRA Testing Panel
- Color-coded buttons by severity:
  - Red: P0 (Critical)
  - Orange: P1 (High)
  - Yellow: P2 (Medium)
- Disabled state for auth-required tests
- Helper text

## 🔌 API Integration

The frontend connects to the Flask backend at `http://localhost:5000/api`

### Endpoints Used

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `GET /api/books` - List books
- `GET /api/cart` - Get cart
- `POST /api/cart` - Add to cart
- `POST /api/orders` - Create order
- `GET /api/test/error/*` - Trigger errors

## 🎯 Key Features

### State Management
- React hooks (useState, useEffect)
- Local storage for JWT token
- Automatic token injection in API requests

### Error Handling
- Display error messages from backend
- Show success messages for actions
- AIRA error severity display

### Responsive Design
- Mobile-friendly layout
- Tailwind CSS utilities
- Grid system for different screen sizes

## 🔒 Authentication Flow

1. User enters credentials
2. Frontend sends to `/api/auth/login`
3. Backend returns JWT token
4. Token stored in localStorage
5. Token sent with all protected requests
6. User data loaded and displayed

## 🛒 Shopping Flow

1. Browse books
2. Click "Add to Cart"
3. View cart in sidebar
4. Click "Checkout"
5. Order created
6. Cart cleared
7. Success message displayed

## 🧪 Error Testing Flow

1. Click error test button
2. API request sent to test endpoint
3. Backend triggers error
4. Error logged to AIRA
5. Frontend displays error message
6. Success message confirms AIRA logging

## 📝 TypeScript Types

All API responses are typed:

```typescript
interface User {
  id: number;
  email: string;
  username: string;
}

interface Book {
  id: number;
  title: string;
  author: string;
  price: number;
  stock: number;
  // ...
}

interface Cart {
  items: CartItem[];
  total: number;
  item_count: number;
}
```

## 🎨 Styling

### Tailwind CSS Classes Used

- Layout: `container`, `grid`, `flex`
- Spacing: `px-4`, `py-2`, `gap-4`
- Colors: `bg-blue-600`, `text-white`
- Typography: `text-xl`, `font-bold`
- Effects: `shadow-md`, `rounded-lg`, `hover:bg-blue-700`

### Color Scheme

- Primary: Blue (`bg-blue-600`)
- Success: Green (`bg-green-600`)
- Error: Red (`bg-red-600`)
- Warning: Orange/Yellow (`bg-orange-600`, `bg-yellow-600`)

## 🔧 Configuration

### Vite Proxy

The Vite dev server proxies API requests to the backend:

```typescript
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true,
  }
}
```

This allows the frontend to make requests to `/api/*` which are forwarded to the Flask backend.

## 🐛 Troubleshooting

### Issue: Cannot connect to backend

**Solution**: Ensure the Flask backend is running on port 5000

```bash
cd backend
python app.py
```

### Issue: CORS errors

**Solution**: Backend has CORS configured for `http://localhost:5173`. If using a different port, update `backend/config.py`:

```python
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:YOUR_PORT')
```

### Issue: TypeScript errors

**Solution**: Install dependencies

```bash
npm install
```

### Issue: Tailwind styles not working

**Solution**: Ensure PostCSS and Tailwind are configured correctly. Check:
- `tailwind.config.js` exists
- `postcss.config.js` exists
- `index.css` has Tailwind directives

## 📦 Dependencies

### Core
- `react` - UI library
- `react-dom` - React DOM rendering
- `react-router-dom` - Routing (prepared for future use)
- `axios` - HTTP client

### Development
- `vite` - Build tool
- `typescript` - Type safety
- `tailwindcss` - Utility-first CSS
- `@vitejs/plugin-react` - React plugin for Vite

## 🚀 Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

The build output will be in the `dist/` directory.

## 🎓 Learning Points

This frontend demonstrates:

1. **React Hooks** - useState, useEffect for state management
2. **TypeScript** - Type-safe API calls and props
3. **Axios** - HTTP client with interceptors
4. **Tailwind CSS** - Utility-first styling
5. **Vite** - Fast development and building
6. **JWT Authentication** - Token-based auth flow
7. **Error Handling** - User-friendly error messages
8. **Responsive Design** - Mobile-first approach

## 🎯 Next Steps

The frontend is complete and functional! You can:

1. **Start the frontend**: `npm run dev`
2. **Ensure backend is running**: `python backend/app.py`
3. **Open browser**: `http://localhost:5173`
4. **Login** with test credentials
5. **Test AIRA** by clicking error buttons
6. **Check AIRA dashboard** for logged errors

---

**Frontend Complete! Ready to test AIRA integration! 🎉**