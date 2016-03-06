# -*- coding: utf-8 -*-
from . import index
from flask import request, jsonify, session, redirect, render_template
from flask.ext.login import (
    login_required,
    login_user,
    logout_user,
    current_user
)
from model.user import User
from bson import ObjectId
import json


@index.route('/')
def web_index():
    print current_user.is_authenticated
    return render_template('index.html')


@index.route('/register', methods=['POST','GET'])
def register_user():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = json.loads(request.form['data'])
        phone = data['phone']
        password = data['password']
        username = data['username']
        if User.p_col.find_one({User.Field.phone:phone}):
            return jsonify(state=0, reason="手机号已被注册！")
        else:
            u_id = str(ObjectId())
            u=dict(_id=u_id,username=username,phone=phone,password=password)
            User.p_col.insert(u)
            return jsonify(state=1,reason='')


@index.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    else:
        data = json.loads(request.form['data'])
        phone = data['phone']
        pwd = data['password']
        u = User.p_col.find_one({User.Field.phone: phone})
        if u == None:
            return jsonify(state = 0, reason='手机号错误'), 200
        if pwd != u[User.Field.password]:
            return jsonify(state = 0, reason='密码错误'), 200
        remember = request.form.get('remember', 0, type=int)
        login_user(User(**u), remember=remember)
        u_id = current_user['_id']
        u['detail'] = ''
        u['timeTables'] = []
        return jsonify(state=1,user=u)


@index.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('http://ali.superlin.cc:5555/index/login')

@index.route('/search',methods=['GET'])
def search_phone():
    phone = request.args.get('phone','')
    u = User.p_col.find_one({User.Field.phone: phone})
    if u:
        return jsonify(state=1)
    else:
        return jsonify(state=0)
