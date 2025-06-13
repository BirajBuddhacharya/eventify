from .. import db
from datetime import datetime

class BranchAdmin(db.Model):
    __tablename__ = 'branchAdmins'

    user_id = db.Column(db.String, db.ForeignKey('users.fid', ondelete='CASCADE'), primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.branch_id', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<BranchAdmin {self.user_id}>"

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'branch_id': self.branch_id
        }