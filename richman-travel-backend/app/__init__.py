# app/__init__.py - Fixed Flask application factory
from flask import Flask
from config import config_by_name
from app.extensions import db, migrate, cors, limiter
from app.routes import public_bp, admin_bp, auth_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS properly - this is the key fix
    cors.init_app(app, 
                  origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
                  supports_credentials=True,
                  allow_headers=['Content-Type', 'Authorization'],
                  methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    limiter.init_app(app)
    
    # Register blueprints
    app.register_blueprint(public_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Error handlers
    from app.utils.helpers import register_error_handlers
    register_error_handlers(app)
    
    return app
    