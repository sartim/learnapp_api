from flask import jsonify
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import current_user, jwt_required
from app import app


class TotalQuizzesApi(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        print(current_user.quizzes)

        ret = dict(
            count=len(current_user.quizzes)
        )
        results = []
        for v in current_user.quizzes:
            results.append(dict(name=v.name, description=v.description, time_to_take=v.time_to_take,
                                 needs_invite=v.needs_invite, video_url=v.video_url))
        ret.update(results=results)
        return jsonify(ret), 200


app.add_url_rule('/account/user/quizzes/', view_func=TotalQuizzesApi.as_view('total-user-quizzes'),
                 methods=['GET'])
