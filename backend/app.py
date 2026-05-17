from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from aira_handler import setup_aira_logging
from models import db_session, init_db
import logging

# Import blueprints
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.test_routes import test_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Set up CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.FRONTEND_URL,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Set up JWT
    jwt = JWTManager(app)
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set up AIRA logging
    setup_aira_logging(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(test_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {str(error)}", exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    # Teardown database session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Bookstore API with AIRA Integration',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'books': '/api/books',
                'cart': '/api/cart',
                'orders': '/api/orders',
                'test': '/api/test',
                'health': '/api/test/health'
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'aira_enabled': Config.AIRA_ENABLED
        })
    
    return app


# Initialize database on startup
try:
    init_db()
except Exception as e:
    print(f"Database initialization error: {e}")

# Create app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    print("Database initialized successfully!")
    
    print("\n" + "="*60)
    print("Bookstore API with AIRA Integration")
    print("="*60)
    print(f"Server: http://localhost:5000")
    print(f"API Docs: http://localhost:5000/")
    print(f"Health: http://localhost:5000/health")
    print(f"Test Errors: http://localhost:5000/api/test/")
    print(f"AIRA Enabled: {Config.AIRA_ENABLED}")
    if Config.AIRA_ENABLED:
        print(f"AIRA Webhook: {Config.AIRA_WEBHOOK_URL}")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
