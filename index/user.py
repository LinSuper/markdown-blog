# -*- coding: utf-8 -*-
from . import index
from flask import request, jsonify, redirect, render_template
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
from model.user import User
from bson import ObjectId
import json
from md5 import md5
from lib.xss_filtter import XssHtml


@index.route('/')
def web_index():
    active = current_user.is_authenticated
    return render_template('index.html', active=active, index=1)


@index.route('/register', methods=['POST','GET'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = json.loads(request.form['data'])
        email = data['email']
        password = data['password']
        username = data['username']
        xss_filter = XssHtml()
        xss_filter.feed(username)
        username = xss_filter.getHtml()
        if User.p_col.find_one({User.Field.email:email}):
            return jsonify(state=0, reason="邮箱已被注册！")
        else:
            u_id = str(ObjectId())
            pwd = md5(password).hexdigest()
            u=dict(_id=u_id,username=username,email=email,password=pwd)
            User.p_col.insert(u)
            return jsonify(state=1,reason='')


@index.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        data = json.loads(request.form['data'])
        email = data['email']
        pwd = data['password']
        u = User.p_col.find_one({User.Field.email: email})
        if u == None:
            return jsonify(state = 0, reason='邮箱错误'), 200
        if md5(pwd).hexdigest() != u[User.Field.password]:
            return jsonify(state = 0, reason='密码错误'), 200
        remember = request.form.get('remember', 0, type=int)
        login_user(User(**u), remember=remember)
        return jsonify(state=1, reason='登录成功！')


@index.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/index/login')

@index.route('/search',methods=['GET'])
def search_phone():
    email = request.args.get('email','')
    u = User.p_col.find_one({User.Field.email: email})
    if u:
        return jsonify(state=1)
    else:
        return jsonify(state=0)
