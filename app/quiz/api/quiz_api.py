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
        quiz_id = request.args.get('id')
        if quiz_id:
            quiz = Quiz.get_by_id(quiz_id)
            quiz_dict = quiz.__dict__
            del quiz_dict['_sa_instance_state']
            return jsonify(quiz_dict)
        if request.args.get('owned'):
            return jsonify(Quiz.get_owned(page))
        return jsonify(Quiz.get_all(page))

    @cross_origin()
    @jwt_required
    def post(self):
        body = request.data
        keys = ['name', 'description']
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
            creator_id = current_user.id
            video_url = body['video_url']
            try:
                quiz = Quiz(name=name, description=description, creator_id=creator_id, video_url=video_url)
                quiz.create(quiz)
                quiz.save()
                app.logger.debug("Successfully saved quiz")
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
                        .format(current_user=current_user.get_full_name, request_body=body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning('{} made request with invalid fields: \n {}'.format(current_user.get_full_name, body))
                return jsonify(validated['data']), 400
            quiz = Quiz.get_by_id(body['id'])
            current_user_roles = AccountUser.get_current_user_roles()
            if 'TUTOR' in current_user_roles or 'LEARNER' in current_user_roles:
                if quiz.creator_id != current_user.id:
                    return jsonify(message='You are not allowed to update this quiz!'), 403
            if quiz:
                name = body['name'] if 'name' in body else quiz.name
                description = body['description'] if 'description' in body else quiz.description
                video_url = body['video_url'] if 'video_url' in body else quiz.video_url
                time_to_take = body['time_to_take'] if 'time_to_take' in body else quiz.time_to_take
                needs_invite = body['needs_invite'] if 'needs_invite' in body else quiz.needs_invite
                try:
                    quiz.name = name
                    quiz.description = description
                    quiz.video_url = video_url
                    quiz.time_to_take = time_to_take
                    quiz.needs_invite = needs_invite
                    quiz.save()
                    return jsonify(message='Successfully updated!'), 200
                except Exception as e:
                    app.logger.exception('Exception occurred')
                    return jsonify(message='An error occurred. {}'.format(str(e))), 400
            app.logger.warning('{} trying to update quiz details with {} which does not exist'.
                               format(current_user.name, body['id']))
            return jsonify(message='Quiz with id {} does not exist'.format(body['id'])), 404

    @cross_origin()
    @jwt_required
    def delete(self):
        body = request.data
        keys = ['id']
        if not body:
            validated = validator.field_validator(keys, {})
            if not validated["success"]:
                app.logger.warning(
                    '{current_user} made request with invalid fields: \n {request_body}'
                        .format(current_user=current_user.get_full_name, request_body=body))
                return jsonify(validated['data']), 400
        if request.is_json:
            body = request.get_json()
            validated = validator.field_validator(keys, body)
            if not validated["success"]:
                app.logger.warning(
                    '{} made request with invalid fields: \n {}'.format(current_user.get_full_name, body))
                return jsonify(validated['data']), 400
            quiz = Quiz.get_by_id(body['id'])
            current_user_roles = AccountUser.get_current_user_roles()
            if 'TUTOR' in current_user_roles or 'LEARNER' in current_user_roles:
                if quiz.creator_id != current_user.id:
                    return jsonify(message='You are not allowed to delete this quiz!'), 403
            if quiz:
                try:
                    quiz.delete()
                    quiz.save()
                    return jsonify(message='Successfully deleted!'), 200
                except Exception as e:
                    app.logger.exception('Exception occurred')
                    return jsonify(message='An error occurred. {}'.format(str(e))), 400
            app.logger.warning('{} trying to update quiz details with {} which does not exist'.
                               format(current_user.name, body['id']))
            return jsonify(message='Quiz with id {} does not exist'.format(body['id'])), 404


app.add_url_rule('/quiz/', view_func=QuizApi.as_view('quiz'),
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
