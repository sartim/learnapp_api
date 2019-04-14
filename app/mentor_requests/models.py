from app import db
from app.core.models import Base


class MentorRequest(Base):

    __tablename__ = 'mentor_requests'

    sender_id = db.Column(db.Integer, db.ForeignKey('account_users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('account_users.id'))

    sender_user = db.relationship('AccountUser', foreign_keys='MentorRequest.sender_id')
    receiver_user = db.relationship('AccountUser', foreign_keys='MentorRequest.receiver_id')

    def __init__(self, sender_id=None, receiver_id=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id

    def __repr__(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.sender_id, self.receiver_id)
