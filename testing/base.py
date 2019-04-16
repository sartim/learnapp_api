from flask_migrate import Migrate, upgrade
from app import app, db
from app.account.role.models import AccountRole
from app.account.user.models import AccountUser
from app.account.user.role.models import AccountUserRole
from app.quiz.models import Quiz
from app.quiz.question.models import QuizQuestion
from app.quiz.question.answer.models import QuizQuestionAnswer
from app.quiz.question.type.models import QuizQuestionType
from app.quiz.section.models import QuizSection
from app.quiz.status.models import QuizStatus
from app.mentor_requests.models import MentorRequest
from app.quiz.invite.models import QuizInvite
from app.helpers import utils
from app.api_imports import *
from manage import add_roles, add_demo_users, add_quizzes_data, add_question_type_data, add_quiz_questions_data, \
    add_tutorship_requests_data


class Base:
    @classmethod
    def setup_class(cls):
        cls.client = app.test_client()
        with app.app_context():
            Migrate(app, db)
            upgrade()
            db.create_all()

            add_roles()
            add_demo_users()
            add_quizzes_data()
            add_question_type_data()
            add_quiz_questions_data()
            add_tutorship_requests_data()

            r = cls.client.post('/account/generate/jwt/', json=dict(email='demotutor@mail.com', password='qwertytrewq'))
            cls.headers = {'Authorization': 'Bearer {}'.format(r.json['access_token'])}

    @classmethod
    def teardown_class(cls):
        db.drop_all()
        db.engine.execute("DROP TABLE alembic_version")
