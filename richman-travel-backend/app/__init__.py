# app/__init__.py - Flask application factory
from flask import Flask
from config import config_by_name
from app.extensions import db, migrate, cors, limiter
from app.routes import public_bp, admin_bp, auth_bp

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    app.register_blueprint(public_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Error handlers
    from app.utils.helpers import register_error_handlers
    register_error_handlers(app)
    
    return app