from .. import db

class NewsLetter(db.Model):
    __tablename__ = 'newsletters'
    
    newsletter_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    subscribed_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())