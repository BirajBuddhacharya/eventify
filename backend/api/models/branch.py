from .. import db
import datetime
class Branch(db.Model):
    __tablename__ = 'branches'
    branch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    branch_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationships
    # events = db.relationship('Event', back_populates='branch', cascade='all, delete-orphan')
    # admins = db.relationship(
    #     'User', secondary="branch_admins",
    #     back_populates='admin_branches'
    # )

    def __repr__(self):
        return f"<Branch {self.branch_name}>"
    
    def to_dict(self):
        return {
            "branch_id": self.branch_id, 
            "branch_name": self.branch_name, 
            "location": self.location, 
            'created_at': self.created_at, 
        } 
        