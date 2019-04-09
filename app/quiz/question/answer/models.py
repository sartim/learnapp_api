from app import db
from app.account.user.models import AccountUser
from app.quiz.question.models import QuizQuestion


class QuizQuestionAnswer(db.Model):

    __tablename__ = 'quiz_question_answers'

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), primary_key=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship(AccountUser, backref='answer_account_user', lazy=True)
    question = db.relationship(QuizQuestion, backref='quiz_question', lazy=True)

    def __init__(self, user_id=None, role_id=None):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)
