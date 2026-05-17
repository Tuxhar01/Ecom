from flask import Blueprint, request, jsonify
from models import Book, db_session
from auth import jwt_required_with_user, get_current_user
import logging

test_bp = Blueprint('test', __name__, url_prefix='/api/test')
logger = logging.getLogger(__name__)


class DatabaseError(Exception):
    """Custom exception for database errors."""
    pass


class PaymentError(Exception):
    """Custom exception for payment errors."""
    pass


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class StockError(Exception):
    """Custom exception for stock errors."""
    pass


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


@test_bp.route('/error/database', methods=['GET'])
def test_database_error():
    """
    Test endpoint to simulate critical database failure (P0).
    This demonstrates the most severe type of error.
    """
    try:
        # Simulate database connection failure
        db_session.close()
        db_session.bind.dispose()
        
        # Attempt query that will fail
        db_session.query(Book).first()
        
    except Exception as e:
        logger.critical(
            f"Database connection failed: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'error': 'Database connection failed',
            'severity': 'P0',
            'message': 'Critical database error occurred'
        }), 500


@test_bp.route('/error/payment', methods=['POST'])
@jwt_required_with_user
def test_payment_error():
    """
    Test endpoint to simulate payment processing error (P1).
    This demonstrates high-priority business logic errors.
    """
    try:
        data = request.get_json() or {}
        amount = data.get('amount', 99.99)
        payment_method = data.get('payment_method', 'credit_card')
        
        # Simulate payment gateway failure
        raise PaymentError(
            f"Payment gateway timeout for amount ${amount:.2f} using {payment_method}"
        )
        
    except PaymentError as e:
        logger.error(
            f"Payment processing failed: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'error': 'Payment processing failed',
            'severity': 'P1',
            'message': str(e)
        }), 402


@test_bp.route('/error/auth', methods=['GET'])
def test_auth_error():
    """
    Test endpoint to simulate authentication failure (P1).
    This demonstrates security-related errors.
    """
    try:
        # Simulate authentication failure
        raise AuthenticationError("Invalid or expired JWT token")
        
    except AuthenticationError as e:
        logger.error(
            f"Authentication failed: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'error': 'Authentication failed',
            'severity': 'P1',
            'message': str(e)
        }), 401


@test_bp.route('/error/stock', methods=['POST'])
@jwt_required_with_user
def test_stock_error():
    """
    Test endpoint to simulate stock validation error (P2).
    This demonstrates business rule violations.
    """
    try:
        data = request.get_json() or {}
        book_id = data.get('book_id', 1)
        quantity = data.get('quantity', 1000)
        
        # Get book
        book = db_session.query(Book).filter_by(id=book_id).first()
        
        if not book:
            raise ValueError(f"Book with ID {book_id} not found")
        
        # Check stock
        if book.stock < quantity:
            raise StockError(
                f"Insufficient stock for book '{book.title}'. "
                f"Requested: {quantity}, Available: {book.stock}"
            )
        
        return jsonify({'message': 'Stock check passed'}), 200
        
    except (StockError, ValueError) as e:
        logger.warning(
            f"Stock validation failed: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'error': 'Insufficient stock' if isinstance(e, StockError) else 'Book not found',
            'severity': 'P2',
            'message': str(e)
        }), 400


@test_bp.route('/error/validation', methods=['POST'])
def test_validation_error():
    """
    Test endpoint to simulate validation error (P2).
    This demonstrates input validation failures.
    """
    try:
        data = request.get_json() or {}
        
        errors = {}
        
        # Validate email
        email = data.get('email', '')
        if not email or '@' not in email:
            errors['email'] = 'Invalid email format'
        
        # Validate quantity
        quantity = data.get('quantity', -1)
        if quantity < 0:
            errors['quantity'] = 'Must be positive'
        
        # Validate price
        price = data.get('price', -1)
        if price < 0:
            errors['price'] = 'Must be positive'
        
        if errors:
            raise ValidationError(f"Validation failed: {errors}")
        
        return jsonify({'message': 'Validation passed'}), 200
        
    except ValidationError as e:
        logger.warning(
            f"Validation failed: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'error': 'Validation failed',
            'severity': 'P2',
            'message': 'Invalid input data',
            'details': errors
        }), 400


@test_bp.route('/error/generic', methods=['GET'])
def test_generic_error():
    """
    Test endpoint to simulate a generic exception.
    This demonstrates how unexpected errors are handled.
    """
    try:
        # Simulate an unexpected error
        result = 1 / 0  # ZeroDivisionError
        
    except Exception as e:
        logger.error(
            f"Unexpected error occurred: {str(e)}",
            exc_info=True
        )
        return jsonify({
            'error': 'Internal server error',
            'severity': 'P1',
            'message': str(e)
        }), 500


@test_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the application is running.
    Also checks AIRA integration status.
    """
    from config import Config
    
    aira_status = 'enabled' if Config.AIRA_ENABLED else 'disabled'
    
    return jsonify({
        'status': 'healthy',
        'aira_integration': aira_status,
        'aira_webhook': Config.AIRA_WEBHOOK_URL if Config.AIRA_ENABLED else None
    }), 200

# Made with Bob
