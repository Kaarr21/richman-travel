# app/services/analytics_service.py - Analytics calculations
from app.extensions import db
from app.models import SiteVisit, Booking, Destination
from sqlalchemy import func, extract
from datetime import datetime, timedelta

class AnalyticsService:
    @staticmethod
    def get_visit_stats():
        """Calculate visit statistics"""
        now = datetime.utcnow()
        today = now.date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)
        
        daily_visits = SiteVisit.query.filter(
            func.date(SiteVisit.timestamp) == today
        ).count()
        
        weekly_visits = SiteVisit.query.filter(
            SiteVisit.timestamp >= week_ago
        ).count()
        
        monthly_visits = SiteVisit.query.filter(
            SiteVisit.timestamp >= month_ago
        ).count()
        
        yearly_visits = SiteVisit.query.filter(
            SiteVisit.timestamp >= year_ago
        ).count()
        
        return {
            'daily': daily_visits,
            'weekly': weekly_visits,
            'monthly': monthly_visits,
            'yearly': yearly_visits
        }
    
    @staticmethod
    def get_booking_stats():
        """Calculate booking statistics"""
        total_bookings = Booking.query.count()
        pending_bookings = Booking.query.filter_by(status='pending').count()
        confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
        completed_bookings = Booking.query.filter_by(status='completed').count()
        cancelled_bookings = Booking.query.filter_by(status='cancelled').count()
        
        # Monthly booking trends (last 12 months)
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)
        monthly_trends = db.session.query(
            extract('year', Booking.created_at).label('year'),
            extract('month', Booking.created_at).label('month'),
            func.count(Booking.id).label('count')
        ).filter(
            Booking.created_at >= twelve_months_ago
        ).group_by(
            extract('year', Booking.created_at),
            extract('month', Booking.created_at)
        ).order_by(
            extract('year', Booking.created_at),
            extract('month', Booking.created_at)
        ).all()
        
        return {
            'total': total_bookings,
            'pending': pending_bookings,
            'confirmed': confirmed_bookings,
            'completed': completed_bookings,
            'cancelled': cancelled_bookings,
            'monthly_trends': [
                {
                    'year': int(trend.year),
                    'month': int(trend.month),
                    'count': trend.count
                } for trend in monthly_trends
            ]
        }
    
    @staticmethod
    def get_popular_destinations():
        """Get most popular destinations by bookings and views"""
        # Most booked destinations
        popular_by_bookings = db.session.query(
            Booking.destination,
            func.count(Booking.id).label('bookings')
        ).filter(
            Booking.destination.isnot(None),
            Booking.destination != ''
        ).group_by(Booking.destination).order_by(
            func.count(Booking.id).desc()
        ).limit(10).all()
        
        # Most viewed destinations
        popular_by_views = db.session.query(
            Destination.name,
            Destination.view_count
        ).order_by(Destination.view_count.desc()).limit(10).all()
        
        return {
            'by_bookings': [
                {'destination': dest, 'count': count} 
                for dest, count in popular_by_bookings
            ],
            'by_views': [
                {'destination': name, 'count': views} 
                for name, views in popular_by_views
            ]
        }
    
    @staticmethod
    def get_revenue_stats():
        """Calculate revenue statistics"""
        # Total estimated revenue
        total_revenue = db.session.query(
            func.sum(Booking.estimated_cost)
        ).filter(
            Booking.status.in_(['confirmed', 'completed']),
            Booking.estimated_cost.isnot(None)
        ).scalar() or 0
        
        # Monthly revenue trends
        monthly_revenue = db.session.query(
            extract('year', Booking.created_at).label('year'),
            extract('month', Booking.created_at).label('month'),
            func.sum(Booking.estimated_cost).label('revenue')
        ).filter(
            Booking.status.in_(['confirmed', 'completed']),
            Booking.estimated_cost.isnot(None)
        ).group_by(
            extract('year', Booking.created_at),
            extract('month', Booking.created_at)
        ).order_by(
            extract('year', Booking.created_at),
            extract('month', Booking.created_at)
        ).all()
        
        return {
            'total': float(total_revenue),
            'monthly_trends': [
                {
                    'year': int(trend.year),
                    'month': int(trend.month),
                    'revenue': float(trend.revenue or 0)
                } for trend in monthly_revenue
            ]
        }
        