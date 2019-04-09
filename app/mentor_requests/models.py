from app import db
from app.core.models import Base


class MentorRequest(Base):

    __tablename__ = 'mentor_requests'

    sender_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)
