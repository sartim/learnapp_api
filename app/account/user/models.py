import os

from flask_jwt_extended import current_user
from sqlalchemy import desc
from app.account.user.authenticated.models import AccountUserAuthenticated
from app.account.user.role.models import AccountUserRole
from app.core.mixins import SearchableMixin
from app.core.models import Base
from app import db
from app.helpers import utils


class AccountUser(Base, SearchableMixin):

    __tablename__ = 'account_users'
    __searchable__ = ['first_name', 'middle_name','last_name', 'email', 'phone']

    first_name = db.Column(db.String(255))
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=True)
    phone = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    token = db.Column(db.String(255), nullable=True)
    image = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=False)

    roles = db.relationship(AccountUserRole, backref='account_user_roles', cascade="save-update, merge, delete",
                            lazy=True)
    sessions = db.relationship(AccountUserAuthenticated, backref='account_user_sessions', cascade="save-update, merge, "
                                                                                                  "delete", lazy=True)
    quizzes = db.relationship('Quiz', backref='quiz_statuses', lazy=True)


    def __init__(self, first_name=None, middle_name=None, last_name=None, email=None, phone=None, password=None,
                 token=None, image=None, is_active=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password
        self.token = token
        self.image = image
        self.is_active = is_active

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)

    def get_full_name(self):
        """
        Returns user full name
        :return:
        """
        return "{} {}".format(self.first_name, self.last_name)

    @classmethod
    def get_online_users(cls):
        sessions = AccountUserAuthenticated.get_all()
        if sessions:
            results = []
            for session in sessions:
                user = AccountUser.get_by_id(session.user_id)
                results.append({"id": user.id, "name": "{} {}".format(user.first_name, user.last_name)})
            data = {"count": len(results), "results": results}
            return data
        return None

    @classmethod
    def get_current_user_roles(cls):
        return [v.role.name for v in current_user.roles]

    @classmethod
    def get_user_by_email(cls, email):
        """
        Get user by email
        :return:
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_phone(cls, phone):
        """
        Get user by email
        :return:
        """
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def get_all(cls, page):
        paginated_objs =  cls.query.order_by(desc(cls.created_date)) \
            .paginate(page=page, per_page=int(os.environ.get('PAGINATE_BY')), error_out=False)
        return cls.response(paginated_objs, '/quiz/')

    @classmethod
    def response(cls, paginated_objs, url):
        results = []
        for obj in paginated_objs.items:
            data = dict(
                id=obj.id, first_name=obj.first_name, middle_name=obj.middle_name, last_name=obj.last_name,
                email=obj.email, phone=obj.phone, roles=[v.role.name for v in obj.roles] if obj.roles else [],
                is_active=obj.is_active
            )
            results.append(data)
        data = utils.response_dict(paginated_objs, results, url)
        return data
