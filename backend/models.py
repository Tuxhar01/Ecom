from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.query = db_session.query_property()


class User(Base):
    """User model for authentication and orders."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    cart_items = relationship('Cart', back_populates='user', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    
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
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Book(Base):
    """Book model for the catalog."""
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    description = Column(Text)
    cover_image = Column(String(255))
    isbn = Column(String(13), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    cart_items = relationship('Cart', back_populates='book')
    order_items = relationship('OrderItem', back_populates='book')
    
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
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Cart(Base):
    """Shopping cart model."""
    __tablename__ = 'cart'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='cart_items')
    book = relationship('Book', back_populates='cart_items')
    
    def to_dict(self):
        """Convert cart item to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book': self.book.to_dict() if self.book else None,
            'quantity': self.quantity,
            'subtotal': self.book.price * self.quantity if self.book else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Order(Base):
    """Order model."""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default='pending')  # pending, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert order to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'status': self.status,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class OrderItem(Base):
    """Order items model."""
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at time of order
    
    # Relationships
    order = relationship('Order', back_populates='items')
    book = relationship('Book', back_populates='order_items')
    
    def to_dict(self):
        """Convert order item to dictionary."""
        return {
            'id': self.id,
            'book': self.book.to_dict() if self.book else None,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.price * self.quantity
        }


def init_db():
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def drop_db():
    """Drop all tables."""
    Base.metadata.drop_all(bind=engine)
    print("Database dropped successfully!")


if __name__ == '__main__':
    init_db()

# Made with Bob
