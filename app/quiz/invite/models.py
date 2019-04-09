from app import db
from app.account.user.models import AccountUser
from app.quiz.question.models import QuizQuestion
from app.quiz.status.models import QuizStatus


class QuizInvite(db.Model):
    __tablename__ = 'quiz_assigned'

    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    token = db.Column(db.Text, nullable=True)
    expiry = db.Column(db.DateTime, nullable=True)
    time_taken = db.Column(db.Integer, nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('quiz_statuses.id'), primary_key=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship(AccountUser, backref='assigned_account_user', lazy=True)
    question = db.relationship(QuizQuestion, backref='assigned_quiz_question', lazy=True)
    status = db.relationship(QuizStatus, backref='quiz_statuses', lazy=True)

    def __init__(self, quiz_id=None, user_id=None, token=None, expiry=None, time_taken=None, status_id=None):
        self.quiz_id = quiz_id
        self.user_id = user_id
        self.token = token
        self.expiry = expiry
        self.time_taken = time_taken
        self.status_id = status_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)