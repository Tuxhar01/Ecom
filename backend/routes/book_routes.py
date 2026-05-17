from flask import Blueprint, request, jsonify
from models import Book
from auth import jwt_required_with_user
import logging

book_bp = Blueprint('books', __name__, url_prefix='/api/books')
logger = logging.getLogger(__name__)


@book_bp.route('', methods=['GET'])
def get_books():
    """Get all books with optional search and pagination."""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '', type=str)
        
        # Get all books
        all_books = Book.get_all()
        
        # Apply search filter
        if search:
            search_lower = search.lower()
            all_books = [
                book for book in all_books
                if search_lower in book.title.lower() or search_lower in book.author.lower()
            ]
        
        # Get total count
        total = len(all_books)
        
        # Apply pagination
        start = (page - 1) * per_page
        end = start + per_page
        books = all_books[start:end]
        
        return jsonify({
            'books': [book.to_dict() for book in books],
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch books'}), 500


@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a single book by ID."""
    try:
        book = Book.get_by_id(book_id)
        
        if not book:
            logger.warning(f"Book not found: ID {book_id}")
            raise ValueError(f"Book with ID {book_id} not found")
        
        return jsonify(book.to_dict()), 200
        
    except ValueError as e:
        logger.warning(f"Invalid book ID requested: {str(e)}", exc_info=True)
        return jsonify({'error': str(e), 'severity': 'P2'}), 404
    except Exception as e:
        logger.error(f"Error fetching book {book_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch book'}), 500


@book_bp.route('', methods=['POST'])
@jwt_required_with_user
def create_book():
    """Create a new book (admin only - simplified for demo)."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'author', 'price', 'stock']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create book
        book = Book(
            title=data['title'],
            author=data['author'],
            price=data['price'],
            stock=data['stock'],
            description=data.get('description', ''),
            cover_image=data.get('cover_image', ''),
            isbn=data.get('isbn', '')
        )
        book.save()
        
        logger.info(f"New book created: {book.title}")
        
        return jsonify(book.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error creating book: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to create book'}), 500


@book_bp.route('/<int:book_id>', methods=['PUT'])
@jwt_required_with_user
def update_book(book_id):
    """Update a book (admin only - simplified for demo)."""
    try:
        book = Book.get_by_id(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'price' in data:
            book.price = data['price']
        if 'stock' in data:
            book.stock = data['stock']
        if 'description' in data:
            book.description = data['description']
        if 'cover_image' in data:
            book.cover_image = data['cover_image']
        if 'isbn' in data:
            book.isbn = data['isbn']
        
        book.save()
        
        logger.info(f"Book updated: {book.title}")
        
        return jsonify(book.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error updating book {book_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to update book'}), 500


@book_bp.route('/<int:book_id>', methods=['DELETE'])
@jwt_required_with_user
def delete_book(book_id):
    """Delete a book (admin only - simplified for demo)."""
    try:
        book = Book.get_by_id(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        title = book.title
        # Remove from books_db
        from models import books_db
        if book_id in books_db:
            del books_db[book_id]
        
        logger.info(f"Book deleted: {title}")
        
        return jsonify({'message': 'Book deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error deleting book {book_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to delete book'}), 500

# Made with Bob
