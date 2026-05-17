from flask import Blueprint, request, jsonify
from models import Order, OrderItem, Cart, Book, db_session
from auth import jwt_required_with_user, get_current_user
import logging

order_bp = Blueprint('orders', __name__, url_prefix='/api/orders')
logger = logging.getLogger(__name__)


class PaymentError(Exception):
    """Custom exception for payment errors."""
    pass


@order_bp.route('', methods=['GET'])
@jwt_required_with_user
def get_orders():
    """Get current user's orders."""
    try:
        user = get_current_user()
        
        orders = db_session.query(Order).filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'orders': [order.to_dict() for order in orders]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching orders: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch orders'}), 500


@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required_with_user
def get_order(order_id):
    """Get a specific order."""
    try:
        user = get_current_user()
        
        order = db_session.query(Order).filter_by(
            id=order_id,
            user_id=user.id
        ).first()
        
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        return jsonify(order.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to fetch order'}), 500


@order_bp.route('', methods=['POST'])
@jwt_required_with_user
def create_order():
    """Create order from cart items."""
    try:
        user = get_current_user()
        
        # Get cart items
        cart_items = db_session.query(Cart).filter_by(user_id=user.id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Validate stock for all items
        for item in cart_items:
            if item.book.stock < item.quantity:
                logger.warning(
                    f"Insufficient stock for book '{item.book.title}'. "
                    f"Requested: {item.quantity}, Available: {item.book.stock}"
                )
                return jsonify({
                    'error': 'Insufficient stock',
                    'severity': 'P2',
                    'book': item.book.title,
                    'requested': item.quantity,
                    'available': item.book.stock
                }), 400
        
        # Calculate total
        total_amount = sum(item.book.price * item.quantity for item in cart_items)
        
        # Simulate payment processing (this is where payment errors can occur)
        try:
            # In a real app, this would call a payment gateway
            # For demo, we'll simulate occasional failures
            import random
            if random.random() < 0.1:  # 10% chance of payment failure for testing
                raise PaymentError(f"Payment gateway timeout for amount ${total_amount:.2f}")
        except PaymentError as e:
            logger.error(f"Payment processing failed: {str(e)}", exc_info=True)
            return jsonify({
                'error': 'Payment processing failed',
                'severity': 'P1',
                'message': str(e)
            }), 402
        
        # Create order
        order = Order(
            user_id=user.id,
            total_amount=total_amount,
            status='completed'
        )
        db_session.add(order)
        db_session.flush()  # Get order ID
        
        # Create order items and update stock
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                book_id=item.book_id,
                quantity=item.quantity,
                price=item.book.price
            )
            db_session.add(order_item)
            
            # Update book stock
            item.book.stock -= item.quantity
        
        # Clear cart
        db_session.query(Cart).filter_by(user_id=user.id).delete()
        
        db_session.commit()
        
        logger.info(f"Order {order.id} created for user {user.id}")
        
        return jsonify(order.to_dict()), 201
        
    except PaymentError:
        # Already handled above
        db_session.rollback()
        raise
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error creating order: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to create order'}), 500

# Made with Bob
