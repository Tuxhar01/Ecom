from functools import wraps
from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models import User


def jwt_required_with_user(fn):
    """
    Decorator that requires JWT and loads user into g.
    Also sets user_id and user_email for AIRA context.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        
        # Load user from in-memory storage
        user = User.get_by_id(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        # Store in g for access in routes and AIRA handler
        g.user = user
        g.user_id = user.id
        g.user_email = user.email
        
        return fn(*args, **kwargs)
    
    return wrapper


def get_current_user():
    """Get the current authenticated user from g."""
    return getattr(g, 'user', None)

# Made with Bob
