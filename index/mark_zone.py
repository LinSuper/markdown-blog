# -*- coding: utf-8 -*-
from . import index
from flask import render_template, jsonify, abort, request
from flask_login import current_user, login_required
from functools import wraps
from model.article import Article
from model.user import User
from lib.timehelper import utc2local, datetime2string


@index.route('/MarkZone', methods=['GET'])
def mark_zone():
    current_user_id = current_user.get_id()
    login = current_user.is_authenticated
    if login:
        find_user = User.p_col.find_one(current_user_id)
        user_name = find_user[User.Field.username]
        return render_template('MarkZone.html', index=2, login=login, user_name=user_name)
    else:
        return render_template('MarkZone.html', index=2, login=login)


@index.route('/MarkZone/article', methods=['GET'])
def get_markzone_article():
    article_type = request.args.get('type', 0, type=int)
    start = request.args.get('start', 0, type=int)
    end = request.args.get('end', 5, type=int)
    login = current_user.is_authenticated
    current_user_id = current_user.get_id()
    if login and article_type == 1:
        return ''
    else:
        if article_type == 1:
            return jsonify(stat=0, message='请先登录！')
        if article_type == 0:
            find_articles = Article.p_col.find().sort(
                                Article.Field.create_time, -1
                            )
            count = find_articles.count()
            find_articles = list(find_articles.skip(start).limit(end - start))


        elif article_type == 2:
            find_articles = Article.p_col.find({
                                Article.Field.user_id: {'$exists': True}
                            }).sort(Article.Field.create_time, -1)
            count = find_articles.count()
            find_articles = list(find_articles.skip(start).limit(end - start))
        user_id_list = []
        for i in find_articles:
            if Article.Field.user_id in i:
                user_id_list.append(
                    i[Article.Field.user_id]
                )
        find_user = User.p_col.find({'_id': {'$in': user_id_list}})
        user_dict = {i['_id']:i for i in find_user}
        result = []
        for i in find_articles:
            temp = {}
            create_time = datetime2string(utc2local(i[Article.Field.create_time]))
            temp['create_time'] = create_time
            content = i[Article.Field.content].splitlines()[:2]
            temp['content'] = '\n'.join(content)
            if Article.Field.user_id in i:
                temp['user_id'] = i[Article.Field.user_id]
                temp['user_name'] = user_dict[i[Article.Field.user_id]][User.Field.username]
            else:
                temp['user_id'] = ''
                temp['user_name'] = u'游客'
            temp['title'] = i['title']
            temp['article_id'] = i['_id']
            result.append(temp)
        return jsonify(stat=1, data=result, count=count)