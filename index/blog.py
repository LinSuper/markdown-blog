# -*- coding: utf-8 -*-
from . import index
from flask import render_template, jsonify, abort, request, redirect
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
        'article.html',
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


@index.route('/myself', methods=['GET'])
def redirect_my_blog():
    current_user_id = current_user.get_id()
    login = current_user.is_authenticated
    if login:
        return redirect('/index/blog/' + current_user_id)
    else:
        return redirect('/index/login')


@index.route('/blog/<user_id>')
def show_blog(user_id):
    return render_template('blog.html', index=3, user_id=user_id)

@index.route('/blog/article/<user_id>', methods=['GET'])
def show_blog_article(user_id):
    start = request.args.get('start', 0, type=int)
    end = request.args.get('end', 5, type=int)
    find_article = Article.p_col.find({Article.Field.user_id: user_id}).sort(
        Article.Field.create_time, -1
    )
    count = find_article.count()
    find_article = list(find_article.skip(start).limit(end - start))
    result = []
    for i in find_article:
        temp = {}
        create_time = datetime2string(utc2local(i[Article.Field.create_time]))
        temp['create_time'] = create_time
        content = i[Article.Field.content].splitlines()[:2]
        temp['content'] = '\n'.join(content)
        temp['title'] = i['title']
        temp['article_id'] = i['_id']
        result.append(temp)
    return jsonify(stat=1,data=result,count=count)