from app.core.models import Base
from app import db


class QuizRating(Base):

    __tablename__ = 'quiz_ratings'

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    rating = db.Column(db.Float)
    review = db.Column(db.Text, nullable=True)

    def __init__(self, user_id=None, rating=None, review=None):
        self.user_id = user_id
        self.rating = rating
        self.review = review

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)