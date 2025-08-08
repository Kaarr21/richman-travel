# app/routes/__init__.py
from .public import public_bp
from .admin import admin_bp
from .auth import auth_bp

__all__ = ['public_bp', 'admin_bp', 'auth_bp']