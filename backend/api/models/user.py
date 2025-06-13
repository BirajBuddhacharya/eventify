from .. import db 
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    fid = db.Column(db.String, primary_key=True)
    role = db.Column(db.Enum('normal', 'club', 'admin', name='user_role_enum'), nullable=False, default='normal')
    imageUrl = db.Column(db.String, nullable=True)
    # Relationships
    # event_views = db.relationship('EventView', back_populates='user')
    # admin_branches = db.relationship(
    #     'Branch', secondary='branch_admins',
    #     back_populates='admins'
    # )

    def __repr__(self):
        return f"<User {self.fid}>"

    def to_dict(self):
        return {
            'fid': self.fid,
            'role': self.role,
            'imageUrl': self.imageUrl
        }
