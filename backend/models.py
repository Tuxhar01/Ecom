from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import threading

# Thread-safe in-memory storage
_lock = threading.Lock()

# In-memory data stores
users_db = {}
books_db = {}
cart_db = {}
orders_db = {}
order_items_db = {}

# Auto-increment IDs
_user_id_counter = 1
_book_id_counter = 1
_cart_id_counter = 1
_order_id_counter = 1
_order_item_id_counter = 1


class User:
    """User model for authentication and orders."""
    
    def __init__(self, email, username, password=None, id=None):
        global _user_id_counter
        with _lock:
            self.id = id if id else _user_id_counter
            if not id:
                _user_id_counter += 1
        
        self.email = email
        self.username = username
        self.password_hash = None
        if password:
            self.set_password(password)
        self.created_at = datetime.utcnow()
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary (excluding password)."""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }
    
    def save(self):
        """Save user to in-memory database."""
        users_db[self.id] = self
        return self
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID."""
        return users_db.get(user_id)
    
    @staticmethod
    def get_by_email(email):
        """Get user by email."""
        for user in users_db.values():
            if user.email == email:
                return user
        return None
    
    @staticmethod
    def get_by_username(username):
        """Get user by username."""
        for user in users_db.values():
            if user.username == username:
                return user
        return None


class Book:
    """Book model for the catalog."""
    
    def __init__(self, title, author, price, stock=0, description='', cover_image='', isbn='', id=None):
        global _book_id_counter
        with _lock:
            self.id = id if id else _book_id_counter
            if not id:
                _book_id_counter += 1
        
        self.title = title
        self.author = author
        self.price = price
        self.stock = stock
        self.description = description
        self.cover_image = cover_image
        self.isbn = isbn
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert book to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'stock': self.stock,
            'description': self.description,
            'cover_image': self.cover_image,
            'isbn': self.isbn,
            'created_at': self.created_at.isoformat()
        }
    
    def save(self):
        """Save book to in-memory database."""
        books_db[self.id] = self
        return self
    
    @staticmethod
    def get_by_id(book_id):
        """Get book by ID."""
        return books_db.get(book_id)
    
    @staticmethod
    def get_all():
        """Get all books."""
        return list(books_db.values())
    
    @staticmethod
    def search(query):
        """Search books by title or author."""
        query = query.lower()
        results = []
        for book in books_db.values():
            if query in book.title.lower() or query in book.author.lower():
                results.append(book)
        return results


class Cart:
    """Shopping cart model."""
    
    def __init__(self, user_id, book_id, quantity=1, id=None):
        global _cart_id_counter
        with _lock:
            self.id = id if id else _cart_id_counter
            if not id:
                _cart_id_counter += 1
        
        self.user_id = user_id
        self.book_id = book_id
        self.quantity = quantity
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert cart item to dictionary."""
        book = Book.get_by_id(self.book_id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book': book.to_dict() if book else None,
            'quantity': self.quantity,
            'subtotal': book.price * self.quantity if book else 0,
            'created_at': self.created_at.isoformat()
        }
    
    def save(self):
        """Save cart item to in-memory database."""
        cart_db[self.id] = self
        return self
    
    def delete(self):
        """Delete cart item."""
        if self.id in cart_db:
            del cart_db[self.id]
    
    @staticmethod
    def get_by_id(cart_id):
        """Get cart item by ID."""
        return cart_db.get(cart_id)
    
    @staticmethod
    def get_by_user(user_id):
        """Get all cart items for a user."""
        return [item for item in cart_db.values() if item.user_id == user_id]
    
    @staticmethod
    def get_by_user_and_book(user_id, book_id):
        """Get cart item by user and book."""
        for item in cart_db.values():
            if item.user_id == user_id and item.book_id == book_id:
                return item
        return None
    
    @staticmethod
    def clear_user_cart(user_id):
        """Clear all items from user's cart."""
        items_to_delete = [item_id for item_id, item in cart_db.items() if item.user_id == user_id]
        for item_id in items_to_delete:
            del cart_db[item_id]


class Order:
    """Order model."""
    
    def __init__(self, user_id, total_amount, status='pending', id=None):
        global _order_id_counter
        with _lock:
            self.id = id if id else _order_id_counter
            if not id:
                _order_id_counter += 1
        
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert order to dictionary."""
        items = OrderItem.get_by_order(self.id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'items': [item.to_dict() for item in items],
            'created_at': self.created_at.isoformat()
        }
    
    def save(self):
        """Save order to in-memory database."""
        orders_db[self.id] = self
        return self
    
    @staticmethod
    def get_by_id(order_id):
        """Get order by ID."""
        return orders_db.get(order_id)
    
    @staticmethod
    def get_by_user(user_id):
        """Get all orders for a user."""
        return [order for order in orders_db.values() if order.user_id == user_id]


class OrderItem:
    """Order items model."""
    
    def __init__(self, order_id, book_id, quantity, price, id=None):
        global _order_item_id_counter
        with _lock:
            self.id = id if id else _order_item_id_counter
            if not id:
                _order_item_id_counter += 1
        
        self.order_id = order_id
        self.book_id = book_id
        self.quantity = quantity
        self.price = price
    
    def to_dict(self):
        """Convert order item to dictionary."""
        book = Book.get_by_id(self.book_id)
        return {
            'id': self.id,
            'book': book.to_dict() if book else None,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.price * self.quantity
        }
    
    def save(self):
        """Save order item to in-memory database."""
        order_items_db[self.id] = self
        return self
    
    @staticmethod
    def get_by_order(order_id):
        """Get all items for an order."""
        return [item for item in order_items_db.values() if item.order_id == order_id]


# Dummy session object for compatibility
class DummySession:
    """Dummy session object to maintain API compatibility."""
    
    def remove(self):
        pass
    
    def commit(self):
        pass
    
    def rollback(self):
        pass


db_session = DummySession()


def init_db():
    """Initialize the in-memory database with sample data."""
    print("Initializing in-memory database...")
    # Data is already initialized in memory
    print("In-memory database ready!")


def drop_db():
    """Clear all in-memory data."""
    global users_db, books_db, cart_db, orders_db, order_items_db
    users_db.clear()
    books_db.clear()
    cart_db.clear()
    orders_db.clear()
    order_items_db.clear()
    print("In-memory database cleared!")


if __name__ == '__main__':
    init_db()

# Made with Bob
