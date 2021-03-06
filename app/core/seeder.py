import os
import json

from app import db, app
from app.account.role.models import AccountRole
from app.account.user.models import AccountUser
from app.account.user.role.models import AccountUserRole
from app.helpers import utils
from app.mentor_requests.models import MentorRequest
from app.quiz.models import Quiz
from app.quiz.question.type.models import QuizQuestionType
from app.quiz.section.models import QuizSection
from app.quiz.status.models import QuizStatus



def get_test_data(file):
    test_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','data', file))
    with open(test_data_path) as f:
        data = json.load(f)
    return data


class QuizSeeder:
    def __init__(self, name, creator_id, video_url, description, time_to_take, needs_invite, section_id, questions):
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.video_url = video_url
        self.time_to_take = time_to_take
        self.needs_invite = needs_invite
        self.section_id = section_id
        self.questions = questions

    def create_quiz(self):
        quiz = Quiz(name=self.name, description=self.description, creator_id=self.creator_id, video_url=self.video_url,
             time_to_take=self.time_to_take, needs_invite=self.needs_invite, section_id=self.section_id)
        db.session.add(quiz)
        quiz.save()

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'.format(cls.__name__))
        except Exception:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__))


class UserSeeder:
    def __init__(self, first_name, last_name, email, phone, password, roles, user_id=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = utils.generate_password_hash(password)
        self.is_active = True
        self.roles = roles

    def create_user(self):
        user = AccountUser(first_name=self.first_name, last_name=self.last_name, email=self.email,
                           phone=self.phone, password=self.password, is_active=self.is_active)
        db.session.add(user)
        user.save()
        return user

    def create_user_and_roles(self):
        user = self.create_user()
        self.user_id = user.id
        self.roles = self.roles
        self.create_user_roles()

    def create_user_roles(self):
        for role in self.roles:
            r = AccountRole.get_or_create(role=role)
            AccountUserRole.get_or_create(user_id=self.user_id, role_id=r.id)

    @classmethod
    def save(cls):
        try:
            db.session.commit()
            app.logger.debug('Successfully committed {} instance'.format(cls.__name__))
        except Exception:
            app.logger.exception('Exception occurred. Could not save {} instance.'.format(cls.__name__))

def add_roles():
    objects = [
        AccountRole(name='SUPERUSER'), AccountRole(name='ADMIN'), AccountRole(name='TUTOR'),
        AccountRole(name='LEARNER')
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()



def add_question_type():
    objects = [QuizQuestionType(name="open"), QuizQuestionType(name="multichoice")]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_quiz_sections():
    objects = [QuizSection(name="Programming"), QuizSection(name="Software Development")]
    db.session.bulk_save_objects(objects)
    db.session.commit()


def add_quiz_statuses():
    QuizStatus.get_or_create_by_name('DRAFT')
    QuizStatus.get_or_create_by_name('COMPLETE')


def add_users():
    data = get_test_data('user_data.json')
    for v in data:
        UserSeeder(first_name=v['first_name'], last_name=v['last_name'], email=v['email'],
                           phone=v['phone'], password=v['password'], roles=v['roles']).create_user_and_roles()
    print("Finished adding user data!")


def add_quiz():
    data = get_test_data('quiz_data.json')
    for v in data:
        QuizSeeder(name=v['quiz']['name'], creator_id=v['quiz']['creator_id'], video_url=v['quiz']['video_url'],
                   description=v['quiz']['description'], time_to_take=v['quiz']['time_to_take'],
                   needs_invite=v['quiz']['needs_invite'], section_id=v['quiz']['section_id'],
                   questions=v['questions']).create_quiz()

def add_tutorship_requests():
    obj = MentorRequest(sender_id=2, receiver_id=1)
    db.session.add(obj)
    db.session.commit()
