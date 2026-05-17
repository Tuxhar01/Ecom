import { useState, useEffect } from 'react';
import { booksAPI, authAPI, cartAPI, ordersAPI, testAPI } from './services/api';
import type { Book, User, Cart } from './types';
import './index.css';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [books, setBooks] = useState<Book[]>([]);
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  
  // Auth state
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      loadUser();
      loadBooks();
      loadCart();
    } else {
      loadBooks();
    }
  }, []);

  const loadUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (err) {
      localStorage.removeItem('token');
    }
  };

  const loadBooks = async () => {
    try {
      const data = await booksAPI.getBooks(1, 20);
      setBooks(data.books);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load books');
    }
  };

  const loadCart = async () => {
    try {
      const cartData = await cartAPI.getCart();
      setCart(cartData);
    } catch (err) {
      console.error('Failed to load cart');
    }
  };

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      if (isLogin) {
        const data = await authAPI.login(email, password);
        localStorage.setItem('token', data.access_token);
        setUser(data.user);
        setSuccess('Login successful!');
        loadCart();
      } else {
        await authAPI.register(email, username, password);
        setSuccess('Registration successful! Please login.');
        setIsLogin(true);
      }
      setEmail('');
      setPassword('');
      setUsername('');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setCart(null);
    setSuccess('Logged out successfully');
  };

  const handleAddToCart = async (bookId: number) => {
    if (!user) {
      setError('Please login to add items to cart');
      return;
    }
    
    try {
      await cartAPI.addToCart(bookId, 1);
      setSuccess('Added to cart!');
      loadCart();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to add to cart');
    }
  };

  const handleCheckout = async () => {
    if (!cart || cart.items.length === 0) {
      setError('Cart is empty');
      return;
    }
    
    setLoading(true);
    try {
      await ordersAPI.createOrder();
      setSuccess('Order placed successfully!');
      loadCart();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to create order');
    } finally {
      setLoading(false);
    }
  };

  const handleTestError = async (errorType: string) => {
    setLoading(true);
    setError('');
    try {
      switch (errorType) {
        case 'database':
          await testAPI.triggerDatabaseError();
          break;
        case 'payment':
          await testAPI.triggerPaymentError();
          break;
        case 'auth':
          await testAPI.triggerAuthError();
          break;
        case 'stock':
          await testAPI.triggerStockError();
          break;
        case 'validation':
          await testAPI.triggerValidationError();
          break;
      }
    } catch (err: any) {
      const errorData = err.response?.data;
      setError(`${errorData?.error || 'Error triggered'} (Severity: ${errorData?.severity || 'Unknown'})`);
      setSuccess('Error sent to AIRA! Check your dashboard.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">📚 Bookstore - AIRA Demo</h1>
            <div className="flex items-center gap-4">
              {user ? (
                <>
                  <span>Welcome, {user.username}!</span>
                  <span className="bg-blue-700 px-3 py-1 rounded">
                    Cart: {cart?.item_count || 0}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <span>Please login</span>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Messages */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        {success && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {success}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Auth or Cart */}
          <div className="lg:col-span-1">
            {!user ? (
              /* Login/Register Form */
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-bold mb-4">
                  {isLogin ? 'Login' : 'Register'}
                </h2>
                <form onSubmit={handleAuth} className="space-y-4">
                  <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-2 border rounded"
                    required
                  />
                  {!isLogin && (
                    <input
                      type="text"
                      placeholder="Username"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      className="w-full px-4 py-2 border rounded"
                      required
                    />
                  )}
                  <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-2 border rounded"
                    required
                  />
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
                  >
                    {loading ? 'Loading...' : isLogin ? 'Login' : 'Register'}
                  </button>
                </form>
                <button
                  onClick={() => setIsLogin(!isLogin)}
                  className="w-full mt-4 text-blue-600 hover:underline"
                >
                  {isLogin ? 'Need an account? Register' : 'Have an account? Login'}
                </button>
                
                <div className="mt-6 pt-6 border-t">
                  <p className="text-sm text-gray-600 mb-2">Test Credentials:</p>
                  <p className="text-xs text-gray-500">user@example.com / password123</p>
                </div>
              </div>
            ) : (
              /* Shopping Cart */
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-bold mb-4">Shopping Cart</h2>
                {cart && cart.items.length > 0 ? (
                  <>
                    <div className="space-y-2 mb-4">
                      {cart.items.map((item) => (
                        <div key={item.id} className="flex justify-between text-sm">
                          <span>{item.book.title}</span>
                          <span>${item.subtotal.toFixed(2)}</span>
                        </div>
                      ))}
                    </div>
                    <div className="border-t pt-2 mb-4">
                      <div className="flex justify-between font-bold">
                        <span>Total:</span>
                        <span>${cart.total.toFixed(2)}</span>
                      </div>
                    </div>
                    <button
                      onClick={handleCheckout}
                      disabled={loading}
                      className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded"
                    >
                      {loading ? 'Processing...' : 'Checkout'}
                    </button>
                  </>
                ) : (
                  <p className="text-gray-500">Your cart is empty</p>
                )}
              </div>
            )}

            {/* AIRA Error Testing */}
            <div className="bg-white rounded-lg shadow-md p-6 mt-6">
              <h2 className="text-xl font-bold mb-4">🧪 Test AIRA Errors</h2>
              <div className="space-y-2">
                <button
                  onClick={() => handleTestError('database')}
                  className="w-full bg-red-600 hover:bg-red-700 text-white py-2 rounded text-sm"
                >
                  P0: Database Error
                </button>
                <button
                  onClick={() => handleTestError('payment')}
                  className="w-full bg-orange-600 hover:bg-orange-700 text-white py-2 rounded text-sm"
                  disabled={!user}
                >
                  P1: Payment Error
                </button>
                <button
                  onClick={() => handleTestError('auth')}
                  className="w-full bg-orange-600 hover:bg-orange-700 text-white py-2 rounded text-sm"
                >
                  P1: Auth Error
                </button>
                <button
                  onClick={() => handleTestError('stock')}
                  className="w-full bg-yellow-600 hover:bg-yellow-700 text-white py-2 rounded text-sm"
                  disabled={!user}
                >
                  P2: Stock Error
                </button>
                <button
                  onClick={() => handleTestError('validation')}
                  className="w-full bg-yellow-600 hover:bg-yellow-700 text-white py-2 rounded text-sm"
                >
                  P2: Validation Error
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-4">
                Click to trigger errors and check AIRA dashboard
              </p>
            </div>
          </div>

          {/* Right Column - Books */}
          <div className="lg:col-span-2">
            <h2 className="text-2xl font-bold mb-6">Available Books</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {books.map((book) => (
                <div key={book.id} className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="font-bold text-lg mb-2">{book.title}</h3>
                  <p className="text-gray-600 text-sm mb-2">by {book.author}</p>
                  <p className="text-gray-500 text-sm mb-4 line-clamp-2">
                    {book.description}
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-xl font-bold text-blue-600">
                      ${book.price.toFixed(2)}
                    </span>
                    <span className="text-sm text-gray-500">
                      Stock: {book.stock}
                    </span>
                  </div>
                  <button
                    onClick={() => handleAddToCart(book.id)}
                    disabled={!user || book.stock === 0}
                    className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded disabled:bg-gray-400"
                  >
                    {book.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

// Made with Bob
