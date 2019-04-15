from flask import jsonify, request
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, current_user
from app import app
from app.helpers import validator
from app.quiz.question.models import QuizQuestion


class QuizQuestionsApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        page = request.args.get('page')
        questions = QuizQuestion.get_all(page)
        return jsonify(questions)

    @cross_origin()
    @jwt_required
    def post(self):
        body = request.data
        keys = ['quiz_id', 'question', 'question_type_id', 'choices', 'section_id', 'answer']
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
            quiz_id = body['name']
            question = body['description']
            question_type_id = body['question_type_id']
            choices = body['choices']
            section_id = body['section_id']
            answer = body['answer']
            try:
                question = QuizQuestion(quiz_id=quiz_id, question=question, question_type_id=question_type_id,
                                    choices=choices, section_id=section_id, answer=answer)
                question.create(question)
                question.save()
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
                app.logger.warning(
                    '{} made request with invalid fields: \n {}'.format(current_user.get_full_name, body))
                return jsonify(validated['data']), 400
            question = QuizQuestion.get_by_id(body['id'])
            if question:
                quiz_id = body['name']
                question = body['description']
                question_type_id = body['question_type_id']
                choices = body['choices']
                section_id = body['section_id']
                try:
                    question = QuizQuestion(quiz_id=quiz_id, question=question, question_type_id=question_type_id,
                                            choices=choices, section_id=section_id)
                    question.create(question)
                    question.save()
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
                quiz = QuizQuestion.get_by_id(body['id'])
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


app.add_url_rule('/quiz/question', view_func=QuizQuestionsApi.as_view('questions'),
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
