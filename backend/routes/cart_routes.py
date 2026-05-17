from flask import Blueprint, request, jsonify
from models import Cart, Book
from auth import jwt_required_with_user, get_current_user
import logging

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')
logger = logging.getLogger(__name__)


@cart_bp.route('', methods=['GET'])
@jwt_required_with_user
def get_cart():
    """Get current user's cart."""
    try:
        user = get_current_user()
        
        cart_items = Cart.get_by_user(user.id)
        
        total = sum(
            Book.get_by_id(item.book_id).price * item.quantity 
            for item in cart_items 
            if Book.get_by_id(item.book_id)
        )
        
        return jsonify({
            'items': [item.to_dict() for item in cart_items],
            'total': total,
            'item_count': len(cart_items)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching cart: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch cart'}), 500


@cart_bp.route('', methods=['POST'])
@jwt_required_with_user
def add_to_cart():
    """Add item to cart."""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data or 'book_id' not in data:
            return jsonify({'error': 'Book ID is required'}), 400
        
        book_id = data['book_id']
        quantity = data.get('quantity', 1)
        
        # Check if book exists
        book = Book.get_by_id(book_id)
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        # Check stock
        if book.stock < quantity:
            logger.warning(f"Insufficient stock for book {book_id}. Requested: {quantity}, Available: {book.stock}")
            return jsonify({
                'error': 'Insufficient stock',
                'severity': 'P2',
                'available': book.stock
            }), 400
        
        # Check if item already in cart
        cart_item = Cart.get_by_user_and_book(user.id, book_id)
        
        if cart_item:
            # Update quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # Create new cart item
            cart_item = Cart(
                user_id=user.id,
                book_id=book_id,
                quantity=quantity
            )
            cart_item.save()
        
        logger.info(f"User {user.id} added book {book_id} to cart")
        
        return jsonify(cart_item.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error adding to cart: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to add to cart'}), 500


@cart_bp.route('/<int:cart_id>', methods=['PUT'])
@jwt_required_with_user
def update_cart_item(cart_id):
    """Update cart item quantity."""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data or 'quantity' not in data:
            return jsonify({'error': 'Quantity is required'}), 400
        
        quantity = data['quantity']
        
        if quantity < 1:
            return jsonify({'error': 'Quantity must be at least 1'}), 400
        
        # Get cart item
        cart_item = Cart.get_by_id(cart_id)
        
        if not cart_item or cart_item.user_id != user.id:
            return jsonify({'error': 'Cart item not found'}), 404
        
        # Check stock
        book = Book.get_by_id(cart_item.book_id)
        if book and book.stock < quantity:
            logger.warning(f"Insufficient stock for book {cart_item.book_id}")
            return jsonify({
                'error': 'Insufficient stock',
                'severity': 'P2',
                'available': book.stock
            }), 400
        
        cart_item.quantity = quantity
        cart_item.save()
        
        logger.info(f"User {user.id} updated cart item {cart_id}")
        
        return jsonify(cart_item.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error updating cart item: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to update cart item'}), 500


@cart_bp.route('/<int:cart_id>', methods=['DELETE'])
@jwt_required_with_user
def remove_from_cart(cart_id):
    """Remove item from cart."""
    try:
        user = get_current_user()
        
        cart_item = Cart.get_by_id(cart_id)
        
        if not cart_item or cart_item.user_id != user.id:
            return jsonify({'error': 'Cart item not found'}), 404
        
        cart_item.delete()
        
        logger.info(f"User {user.id} removed cart item {cart_id}")
        
        return jsonify({'message': 'Item removed from cart'}), 200
        
    except Exception as e:
        logger.error(f"Error removing from cart: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to remove from cart'}), 500


@cart_bp.route('', methods=['DELETE'])
@jwt_required_with_user
def clear_cart():
    """Clear all items from cart."""
    try:
        user = get_current_user()
        
        Cart.clear_user_cart(user.id)
        
        logger.info(f"User {user.id} cleared cart")
        
        return jsonify({'message': 'Cart cleared'}), 200
        
    except Exception as e:
        logger.error(f"Error clearing cart: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to clear cart'}), 500

# Made with Bob
