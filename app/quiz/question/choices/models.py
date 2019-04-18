from app import db, app
from app.quiz.question.models import QuizQuestion


class QuizQuestionChoice(db.Model):

    ___tablename__ ='quiz_question_choices'

    question_id = db.Column(db.Integer, db.ForeignKey('quiz_questions.id'), primary_key=True)
    choices = db.Column(db.JSON)

    question = db.relationship(QuizQuestion, backref='quiz_question_choice', lazy=True)

    def __init__(self, question_id=None, choices=None):
        self.question_id = question_id
        self.choices = choices

    @staticmethod
    def create(obj):
        db.session.add(obj)
        obj.save()
        return obj

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'.format(cls.__name__))
        except Exception:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__))
