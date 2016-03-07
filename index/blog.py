# -*- coding: utf-8 -*-
from . import index
from flask import render_template, jsonify, abort, request
from flask_login import current_user, login_required
from model.article import Article
from model.user import User
from bson import ObjectId
from datetime import datetime
from lib.timehelper import utc2local, datetime2string


@index.route('/article/<article_id>', methods=['GET'])
def article(article_id):
    current_user_id = current_user.get_id()
    login = current_user.is_authenticated
    find_article = Article.p_col.find_one({'_id': article_id})
    content = find_article['content']
    title = find_article['title']
    create_time = datetime2string(utc2local(find_article['create_time']))
    user_id = find_article.get('user_id', None)
    if user_id:
        find_user = User.p_col.find_one(user_id)
        author = find_user.get(User.Field.username, u'游客')
    else:
        author = u'游客'
    if current_user_id == user_id and user_id != None:
        auth = True
        user_name = author
    else:
        auth = False
        user_name = User.p_col.find_one(current_user_id).get('username', '')
    return render_template(
            'blog.html',
            content=content,
            title=title,
            create_time=create_time,
            author=author,
            index=2,
            login=login,
            auth=auth,
            user_name=user_name,
            article_id=article_id

        )