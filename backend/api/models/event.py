# from api import db 
from datetime import datetime, timezone
from .. import db

class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    is_paid = db.Column(db.Boolean, default=False, nullable=False)
    price = db.Column(db.Numeric(10, 2))    
    max_capacity = db.Column(db.Integer)
    imageUrl = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    # branch = db.relationship('Branch', back_populates='events')
    # registrations = db.relationship('Registration', back_populates='event', cascade='all, delete-orphan')
    # views = db.relationship('EventView', back_populates='event', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Event {self.title} on {self.event_date}>"

    def to_dict(self):
        return {
            'id': self.event_id,
            'branchId': self.branch_id,
            'title': self.title,
            'description': self.description,
            'date': self.event_date.isoformat() if self.event_date else None,
            'location': self.location,
            'isPaid': self.is_paid,
            'price': float(self.price) if self.price else None,
            'maxCapacity': self.max_capacity,
            'imageUrl': self.imageUrl,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        }