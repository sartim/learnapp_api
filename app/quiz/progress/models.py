from app.account.user.models import AccountUser
from app.core.models import Base
from app import db
from app.quiz.models import Quiz
from app.quiz.status.models import QuizStatus


class QuizProgress(Base):

    __tablename__ = 'quiz_progress'

    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('quiz_statuses.id'))
    started_date_time = db.Column(db.DateTime)
    ended_date_time = db.Column(db.DateTime)

    quiz = db.relationship(Quiz, backref='quiz', lazy=True)
    user = db.relationship(AccountUser, backref='account_user', lazy=True)
    status = db.relationship(QuizStatus, backref='quiz_status', lazy=True)


    def __init__(self, quiz_id=None, user_id=None, status_id=None, started_date_time=None, ended_date_time=None):
        self.quiz_id = quiz_id
        self.user_id = user_id
        self.status_id = status_id
        self.started_date_time = started_date_time
        self.ended_date_time = ended_date_time

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)
