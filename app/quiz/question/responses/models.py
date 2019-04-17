from app import db
from app.account.user.models import AccountUser
from app.core.models import Base
from app.quiz.question.models import QuizQuestion


class QuizQuestionResponse(Base):

    __tablename__ = 'quiz_question_responses'

    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'))
    response = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'))

    question = db.relationship(QuizQuestion, backref='quiz_question_response', lazy=True)
    user = db.relationship(AccountUser, backref='quiz_question_response_account_user', lazy=True)

    def __init__(self, question_id=None, response=None, user_id=None):
        self.question_id = question_id
        self.response = response
        self.user_id = user_id
