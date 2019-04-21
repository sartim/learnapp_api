from flask import request, jsonify
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.quiz.section.models import QuizSection


class QuizSectionApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        page = request.args.get('page')
        quiz_id = request.args.get('id')
        if quiz_id:
            quiz = QuizSection.get_by_id(quiz_id)
            quiz_dict = quiz.__dict__
            del quiz_dict['_sa_instance_state']
            return jsonify(quiz_dict)
        return jsonify(QuizSection.get_all(page))


app.add_url_rule('/section/', view_func=QuizSectionApi.as_view('quiz-section'),
                 methods=['GET'])
