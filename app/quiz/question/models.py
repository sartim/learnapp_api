from app import db
from app.core.models import Base
from app.quiz.models import Quiz
from app.quiz.question.type.models import QuizQuestionType
from app.quiz.section.models import QuizSection


class QuizQuestion(Base):

    __tablename__ = 'quiz_questions'

    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'))
    question = db.Column(db.String(255))
    question_type_id = db.Column(db.Integer, db.ForeignKey('quiz_question_types.id'))
    choices = db.Column(db.JSON, nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('quiz_sections.id'))

    quiz = db.relationship(Quiz, backref='quiz', lazy=True)
    type = db.relationship(QuizQuestionType, backref='quiz_question_type', lazy=True)
    section = db.relationship(QuizSection, backref='quiz_section', lazy=True)

    def __init__(self, quiz_id=None, question=None, question_type_id=None, choices=None, section_id=None):
        self.quiz_id = quiz_id
        self.question = question
        self.question_type_id = question_type_id
        self.choices = choices
        self.section_id = section_id
