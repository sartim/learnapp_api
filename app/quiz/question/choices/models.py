from app import db
from app.quiz.question.models import QuizQuestion


class QuizQuestionChoices:

    ___tablename__ ='quiz_question_choices'

    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'))
    choices = db.Column(db.JSON)

    question = db.relationship(QuizQuestion, backref='quiz', lazy=True)

    def __init__(self, choices=None):
        self.choices = choices
