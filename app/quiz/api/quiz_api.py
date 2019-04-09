from flask import request, jsonify
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, current_user
from app import app
from app.account.user.models import AccountUser
from app.helpers import validator
from app.quiz.models import Quiz



class QuizApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        page = request.args.get('page')
        current_user_roles = AccountUser.get_current_user_roles()
        if 'ADMIN' in current_user_roles or 'SUPERUSER' in current_user_roles \
                and 'TUTOR' not in current_user_roles and 'LEARNER' not in current_user_roles:
            return jsonify(Quiz.get_all(page))
        return jsonify(Quiz.get_owned(page))

    @cross_origin()
    def post(self):
        body = request.data
        keys = ['name', 'description', 'creator_id', 'video_url']
        if not body:
            validated = validator.field_validator(keys, {})
            if not validated["success"]:
                app.logger.warning('User made request with invalid fields: \n {}'.format(body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning('User made request with invalid fields: \n {}'.format(body))
                return jsonify(jsonify=validated['data'])
            name = body['name']
            description = body['description']
            creator_id = body['creator_id']
            video_url = body['video_url']
            try:
                quiz = Quiz(name=name, description=description, creator_id=creator_id, video_url=video_url)
                quiz.create(quiz)
                quiz.save()
                app.logger.debug("Successfully saved new user with")
                return jsonify(message="Successfully created!"), 201
            except Exception as e:
                app.logger.exception('Exception occurred')
                return jsonify(message='An error occurred. {}'.format(str(e))), 400
        else:
            app.logger.warning('User submitted request with content type header not being application/json')
            return jsonify(message='Content-type header is not application/json'), 400

    @cross_origin()
    @jwt_required
    def put(self):
        body = request.data
        keys = ['id']
        if not body:
            validated = validator.field_validator(keys, {})
            if not validated["success"]:
                app.logger.warning(
                    '{current_user} made request with invalid fields: \n {request_body}'
                        .format(current_user=current_user.full_name, request_body=body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning('{} made request with invalid fields: \n {}'.format(current_user.full_name, body))
                return jsonify(validated['data']), 400
            quiz = Quiz.get_by_id(body['id'])
            if quiz:
                id = body['id']
                name = body['name'] if 'name' in body else quiz.name
                description = body['description'] if 'description' in body else quiz.description
                video_url = body['video_url'] if 'video_url' in body else quiz.video_url


                try:
                    pass
                except Exception as e:
                    app.logger.exception('Exception occurred')
                    return jsonify(message='An error occurred. {}'.format(str(e))), 400
            app.logger.warning('{} trying to update user details with {} who does not exist'.
                               format(current_user.name, body['id']))
            return jsonify(message='User with id {} does not exist'.format(body['id'])), 404


    @cross_origin()
    @jwt_required
    def delete(self):
        pass


app.add_url_rule('/quiz/', view_func=QuizApi.as_view('quiz'),
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
