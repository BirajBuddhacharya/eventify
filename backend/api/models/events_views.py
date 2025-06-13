from .. import db
from datetime import datetime

class EventView(db.Model):
    __tablename__ = 'event_views'

    view_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    event = db.relationship('Event', back_populates='views')
    user = db.relationship('User', back_populates='event_views')

    def __repr__(self):
        return f"<EventView {self.view_id} on event {self.event_id}>"