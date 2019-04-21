import os

from app import db
from app.core.models import Base
from app.helpers import utils


class QuizSection(Base):

    __tablename__ = 'quiz_sections'

    name = db.Column(db.String(255), unique=True)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls, page):
        paginated_objs = cls.query.paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=False)
        return cls.response(paginated_objs, '/section/')

    @classmethod
    def response(cls, paginated_objs, url):
        results = []
        for obj in paginated_objs.items:
            data = dict(id=obj.id, name=obj.name)
            results.append(data)
        data = utils.response_dict(paginated_objs, results, url)
        return data
