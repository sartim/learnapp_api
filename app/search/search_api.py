import os
from flask import request, jsonify
from flask.views import MethodView
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from app import app
from app.account.user.models import AccountUser
from app.helpers import utils
from app.quiz.models import Quiz


class SearchView(MethodView):
    @cross_origin()
    @jwt_required
    def get(self):
        q = request.args.get('q')
        page = request.args.get('page')
        article_query, article_total = Quiz.search(q, 1, 5)
        account_query, account_total = AccountUser.search(q, 1, 5)
        articles = Quiz.get_all(page)
        accounts = AccountUser.get_all(page)
        if article_total:
            results = utils.MergeDictList([articles, {"type": "quiz"}])
            return jsonify(results)
        if account_total:
            results = utils.MergeDictList([accounts, {"type": "user"}])
            return jsonify(dict_ctx=results)
        results = {"count": 0, "results": []}
        return jsonify(results)



app.add_url_rule('/search/', view_func=SearchView.as_view('search'),
                 methods=['GET'])
