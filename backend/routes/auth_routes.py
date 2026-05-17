from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
import logging

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
logger = logging.getLogger(__name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password') or not data.get('username'):
            logger.warning("Registration attempt with missing fields")
            return jsonify({'error': 'Email, username, and password are required'}), 400
        
        # Check if user already exists
        existing_user = User.get_by_email(data['email'])
        if existing_user:
            logger.warning(f"Registration attempt with existing email: {data['email']}")
            return jsonify({'error': 'User with this email already exists'}), 409
        
        existing_user = User.get_by_username(data['username'])
        if existing_user:
            logger.warning(f"Registration attempt with existing username: {data['username']}")
            return jsonify({'error': 'User with this username already exists'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            username=data['username'],
            password=data['password']
        )
        user.save()
        
        logger.info(f"New user registered: {user.email}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            logger.warning("Login attempt with missing credentials")
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = User.get_by_email(data['email'])
        
        if not user or not user.check_password(data['password']):
            logger.warning(f"Failed login attempt for email: {data['email']}")
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        logger.info(f"User logged in: {user.email}")
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/me', methods=['GET'])
def get_current_user_info():
    """Get current user information (requires JWT)."""
    from flask_jwt_extended import jwt_required, get_jwt_identity
    
    try:
        # Verify JWT
        jwt_required()
        user_id = get_jwt_identity()
        
        # Get user
        user = User.get_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}", exc_info=True)
        return jsonify({'error': 'Failed to get user information'}), 500

# Made with Bob
