import os

from flask_jwt_extended import current_user
from app import db
from app.core.mixins import SearchableMixin
from app.core.models import Base
from app.helpers import utils
from app.quiz.section.models import QuizSection


class Quiz(Base, SearchableMixin):

    __tablename__ = 'quizzes'
    __searchable__ = ['name', 'description']

    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('account_users.id'))
    video_url = db.Column(db.Text, nullable=True)
    time_to_take = db.Column(db.Integer, nullable=True)
    needs_invite = db.Column(db.Boolean, default=False)
    section_id = db.Column(db.Integer, db.ForeignKey('quiz_sections.id'))
    rating = db.Column(db.Integer, nullable=True)

    creator = db.relationship('AccountUser', backref='creator', lazy=True)
    questions = db.relationship('QuizQuestion', backref='quiz_questions', lazy=True)
    section = db.relationship(QuizSection, backref='quiz_section', lazy=True)

    def __init__(self, name=None, description=None, creator_id=None, video_url=None, time_to_take=None,
                 needs_invite=None, section_id=None, rating=None):
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.video_url = video_url
        self.time_to_take = time_to_take
        self.needs_invite = needs_invite
        self.section_id = section_id
        self.rating = rating

    @classmethod
    def response(cls, paginated_objs, url):
        results = []
        for obj in paginated_objs.items:
            data = dict(
                id=obj.id, name=obj.name, description=obj.description, creator=obj.creator.get_full_name(),
                video_url=obj.video_url,
                time_to_take=obj.time_to_take, needs_invite=obj.needs_invite, created_date=obj.created_date
            )
            results.append(data)
        data = utils.response_dict(paginated_objs, results, url)
        return data

    @classmethod
    def get_owned(cls, page):
        """
        Retrieve owned quizzes which belong to the creator
        :param id:
        :param page:
        :return:
        """
        paginated_objs = cls.query.filter_by(creator_id=current_user.id)\
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=False)
        return cls.response(paginated_objs, '/quiz/')

    @classmethod
    def get_all(cls, page):
        """
        Retrieve all quizzes regardless of creator
        :return:
        """
        paginated_objs = cls.query.paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=False)
        return cls.response(paginated_objs, '/quiz/')
