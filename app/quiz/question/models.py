import os

from app import db
from app.core.models import Base
from app.quiz.models import Quiz
from app.quiz.question.type.models import QuizQuestionType
from app.helpers import utils


class QuizQuestion(Base):

    __tablename__ = 'quiz_questions'

    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    order_num = db.column(db.Integer)
    question = db.Column(db.String(255))
    question_type_id = db.Column(db.Integer, db.ForeignKey('quiz_question_types.id'))
    answer = db.Column(db.TEXT)

    quiz = db.relationship(Quiz, backref='quiz_questions_quiz', lazy=True)
    type = db.relationship(QuizQuestionType, backref='quiz_question_type', lazy=True)

    def __init__(self, quiz_id=None, order_num=None, question=None, question_type_id=None, answer=None):
        self.quiz_id = quiz_id
        self.question = question
        self.question_type_id = question_type_id
        self.answer = answer
        self.order_num = order_num

    @classmethod
    def response(cls, paginated_objs, url):
        results = []
        for obj in paginated_objs.items:
            data = dict(
                quiz_id=obj.quiz_id, question=obj.question, question_type_id=obj.question_type_id, choices=obj.choices,
                section_id=obj.section_id, answer=obj.answer
            )
            results.append(data)
        data = utils.response_dict(paginated_objs, results, url)
        return data

    @classmethod
    def get_all(cls, page):
        """
        Retrieve all quizzes regardless of creator
        :return:
        """
        paginated_objs = cls.query.paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=False)
        return cls.response(paginated_objs, '/quiz/')
