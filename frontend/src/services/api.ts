import axios from 'axios';
import type { User, Book, Cart, Order, AuthResponse } from '../types';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: async (email: string, username: string, password: string) => {
    const response = await api.post<{ user: User }>('/auth/register', {
      email,
      username,
      password,
    });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await api.post<AuthResponse>('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get<{ user: User }>('/auth/me');
    return response.data.user;
  },
};

// Books API
export const booksAPI = {
  getBooks: async (page = 1, perPage = 10, search = '') => {
    const response = await api.get<{
      books: Book[];
      total: number;
      page: number;
      per_page: number;
      pages: number;
    }>('/books', {
      params: { page, per_page: perPage, search },
    });
    return response.data;
  },

  getBook: async (id: number) => {
    const response = await api.get<Book>(`/books/${id}`);
    return response.data;
  },
};

// Cart API
export const cartAPI = {
  getCart: async () => {
    const response = await api.get<Cart>('/cart');
    return response.data;
  },

  addToCart: async (bookId: number, quantity = 1) => {
    const response = await api.post('/cart', {
      book_id: bookId,
      quantity,
    });
    return response.data;
  },

  updateCartItem: async (cartId: number, quantity: number) => {
    const response = await api.put(`/cart/${cartId}`, { quantity });
    return response.data;
  },

  removeFromCart: async (cartId: number) => {
    const response = await api.delete(`/cart/${cartId}`);
    return response.data;
  },

  clearCart: async () => {
    const response = await api.delete('/cart');
    return response.data;
  },
};

// Orders API
export const ordersAPI = {
  getOrders: async () => {
    const response = await api.get<{ orders: Order[] }>('/orders');
    return response.data.orders;
  },

  getOrder: async (id: number) => {
    const response = await api.get<Order>(`/orders/${id}`);
    return response.data;
  },

  createOrder: async () => {
    const response = await api.post<Order>('/orders');
    return response.data;
  },
};

// Test API (for triggering errors)
export const testAPI = {
  triggerDatabaseError: async () => {
    const response = await api.get('/test/error/database');
    return response.data;
  },

  triggerPaymentError: async (amount = 99.99) => {
    const response = await api.post('/test/error/payment', { amount });
    return response.data;
  },

  triggerAuthError: async () => {
    const response = await api.get('/test/error/auth');
    return response.data;
  },

  triggerStockError: async (bookId = 1, quantity = 1000) => {
    const response = await api.post('/test/error/stock', {
      book_id: bookId,
      quantity,
    });
    return response.data;
  },

  triggerValidationError: async () => {
    const response = await api.post('/test/error/validation', {
      email: 'invalid-email',
      quantity: -5,
    });
    return response.data;
  },
};

export default api;

// Made with Bob
