from flask import jsonify
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.quiz.models import Quiz


class QuizQuestionsApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self, pk):
        quiz = Quiz.get_by_id(pk)
        questions = quiz.questions
        response_dict = dict(count=len(questions))
        results = []
        for v in questions:
            question_dict = v.__dict__
            del question_dict['_sa_instance_state']
            results.append(question_dict)
        response_dict.update(results=results)
        return jsonify(response_dict)

app.add_url_rule('/quiz/<pk>/questions', view_func=QuizQuestionsApi.as_view('quiz-questions'),
                 methods=['GET', 'POST', 'PUT', 'DELETE'])
