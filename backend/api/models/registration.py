from .. import db
from datetime import datetime, timezone

class Registration(db.Model):
    __tablename__ = 'registrations'

    registration_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(30), db.ForeignKey('users.fid', ondelete='CASCADE'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id', ondelete='CASCADE'), nullable=False)
    registered_at = db.Column(db.DateTime(timezone=True), default=datetime.now(timezone.utc))
    payment_status = db.Column(db.String(20), default='pending')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'event_id', name='uq_user_event'),
    )

    # Relationships
    # user = db.relationship('User', back_populates='registrations')
    # event = db.relationship('Event', back_populates='registrations')

    def __repr__(self):
        return f"<Registration {self.user_id} for {self.event_id}>"

    def to_dict(self):
        return {
            'registration_id': self.registration_id,
            'user_id': self.user_id,
            'event_id': self.event_id,
            'registered_at': self.registered_at.isoformat(),
            'payment_status': self.payment_status
        }