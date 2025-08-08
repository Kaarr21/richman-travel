# app/models.py - Database models
from app.extensions import db
from datetime import datetime
import uuid
import bcrypt
import json

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_reference = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    destination = db.Column(db.String(100))
    preferred_date = db.Column(db.Date)
    guests = db.Column(db.Integer, default=1)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    estimated_cost = db.Column(db.Float)
    google_event_id = db.Column(db.String(255))  # Google Calendar event ID
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def generate_reference(self):
        """Generate unique booking reference"""
        return f"RT{datetime.now().strftime('%Y%m')}{str(uuid.uuid4())[:6].upper()}"

    def to_dict(self):
        return {
            'id': self.id,
            'booking_reference': self.booking_reference,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'destination': self.destination,
            'preferred_date': self.preferred_date.isoformat() if self.preferred_date else None,
            'guests': self.guests,
            'message': self.message,
            'status': self.status,
            'estimated_cost': self.estimated_cost,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Destination(db.Model):
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    duration = db.Column(db.String(50))
    highlights = db.Column(db.Text)  # JSON string
    price_range = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))  # easy, moderate, challenging
    best_time_to_visit = db.Column(db.String(100))
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'duration': self.duration,
            'highlights': json.loads(self.highlights) if self.highlights else [],
            'price_range': self.price_range,
            'difficulty_level': self.difficulty_level,
            'best_time_to_visit': self.best_time_to_visit,
            'is_featured': self.is_featured,
            'view_count': self.view_count,
            'created_at': self.created_at.isoformat()
        }

class SiteVisit(db.Model):
    __tablename__ = 'site_visits'
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))
    page = db.Column(db.String(100))
    user_agent = db.Column(db.String(255))
    referer = db.Column(db.String(255))
    session_id = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat()
        }