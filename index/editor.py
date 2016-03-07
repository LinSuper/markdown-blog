# -*- coding: utf-8 -*-
from . import index
from flask import render_template, jsonify, abort, request
from flask_login import current_user, login_required
from functools import wraps
from model.article import Article
from bson import ObjectId
from datetime import datetime


def auth(user_id, article_id):
    find_article = Article.p_col.find_one(article_id)
    if find_article:
        if find_article.get(Article.Field.user_id, '') == user_id:
            return True, find_article
        else:
            return False, None
    else:
        return False, None


@index.route('/editor', methods=['GET','POST'])
def editor_new():
    if request.method == 'GET':
        return render_template('editor.html', index=2)
    else:
        title = request.form.get('title', '')
        if len(title) <= 1:
            return jsonify(stat=0, message='标题长度太短！')
        content = request.form.get('content', '')
        if len(content) == 0:
            return jsonify(stat=0, message='文章不能为空！')
        article_type = request.form.get('type', 0)
        article_id = str(ObjectId())
        if current_user.is_authenticated:
            Article.p_col.insert({
                '_id': article_id,
                'title': title,
                'content': content,
                Article.Field.type: article_type,
                Article.Field.user_id: current_user.get_id(),
                Article.Field.create_time: datetime.utcnow()
            })
        else:
            Article.p_col.insert({
                '_id': article_id,
                'title': title,
                'content': content,
                Article.Field.type: article_type,
                Article.Field.create_time: datetime.utcnow()
            })
        return jsonify(stat=1, message='发表成功', article_id=article_id)


@login_required
@index.route('/editor/<article_id>', methods=['GET','POST'])
def editor_article(article_id):
    user_id = current_user.get_id()
    is_auth, article = auth(user_id, article_id)
    if not is_auth:
        abort(403)
    if request.method == 'GET':
        return render_template('editor.html', title=article['title'], article=article['content'], index=2)
    else:
        title = request.form.get('title', '')
        if len(title) <= 1:
            return jsonify(stat=0, message='标题长度太短！')
        content = request.form.get('content', '')
        if len(content) == 0:
            return jsonify(stat=0, message='文章不能为空！')
        article_type = request.form.get('type', 0)
        Article.p_col.update({'_id': article_id},{
            '$set': {
                'title': title,
                'content': content,
                Article.Field.type: article_type,
                Article.Field.create_time: datetime.utcnow()
            }
        })
        return jsonify(stat=1, message='发表成功！', article_id=article_id)