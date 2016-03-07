# -*- coding: utf-8 -*-
from . import index
from flask import render_template, jsonify, abort, request
from flask_login import current_user, login_required
from functools import wraps
from model.article import Article
from bson import ObjectId
from datetime import datetime


@index.route('/share/<article_id>', methods=['GET'])
def share_page(article_id):
    return render_template('share.html', link='/index/article/' + article_id, index=2)