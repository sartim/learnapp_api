from app import app, db
from app.account.role.models import AccountRole


class AccountUserRole(db.Model):

    __tablename__ = 'account_user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('account_users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('account_roles.id'), primary_key=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_date = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    user = db.relationship('AccountUser', backref='account_user', lazy=True)
    role = db.relationship(AccountRole, backref='account_role', lazy=True)

    def __init__(self, user_id=None, role_id=None):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.user_id)

    @staticmethod
    def create(obj):
        db.session.add(obj)
        obj.save()
        return obj

    @classmethod
    def get_by_user_and_role(cls, user_id, role_id):
        return cls.query.filter_by(user_id=user_id).filter_by(role_id=role_id).first()

    @classmethod
    def get_or_create(cls, user_id, role_id):
        obj = cls.get_by_user_and_role(user_id, role_id)
        if obj:
            return obj
        obj = cls(user_id, role_id)
        obj.create(obj)
        return obj

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'.format(cls.__name__))
        except Exception:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__))
