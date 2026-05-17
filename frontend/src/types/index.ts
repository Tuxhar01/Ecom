export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface Book {
  id: number;
  title: string;
  author: string;
  price: number;
  stock: number;
  description: string;
  cover_image: string;
  isbn: string;
  created_at: string;
}

export interface CartItem {
  id: number;
  user_id: number;
  book: Book;
  quantity: number;
  subtotal: number;
  created_at: string;
}

export interface Cart {
  items: CartItem[];
  total: number;
  item_count: number;
}

export interface OrderItem {
  id: number;
  book: Book;
  quantity: number;
  price: number;
  subtotal: number;
}

export interface Order {
  id: number;
  user_id: number;
  total_amount: number;
  status: string;
  items: OrderItem[];
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

export interface ApiError {
  error: string;
  severity?: string;
  message?: string;
}

// Made with Bob
