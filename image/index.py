# -*- coding: utf-8 -*-
from . import img
from flask import jsonify, render_template, request
from flask import Response
import requests
import qcloud_cos
from bson import ObjectId
import json


@img.route('/test', methods=['GET'])
def test():
    return render_template('image.html')

@img.route('/zhihu/<img_id>', methods=['GEt'])
def return_zhihu_img(img_id):

    img_url = 'http://pic1.zhimg.com/' + img_id
    header = {'Referer':img_url,'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',':host':'pic1.zhimg.com'
    }
    r = requests.get(img_url)
    return Response(r.content, mimetype='image/jpeg')


@img.route('/sign')
def cos_sign():
    sign_type = request.args.get('sign_type', '')
    bucketName = 'image'
    qcloud_cos.conf.set_app_info('10015041', 'AKID1IT3WdHPa1wa31kUCHy7qzs1l2lzctq7', 'MjsLc89cavUzyRijSXFaPxtwyToZpYue')
    auth = qcloud_cos.Auth('AKID1IT3WdHPa1wa31kUCHy7qzs1l2lzctq7', 'MjsLc89cavUzyRijSXFaPxtwyToZpYue')
    if sign_type == 'appSign':
        if 'expired' not in request.args:
            return jsonify(code=10001,message="缺少expired"), 400
        expired = request.args.get('expired', '')
        sign = auth.sign_more(bucketName, expired)
        return json.dumps(dict(
            code="0", message='成功', data={'sign': sign}, key=str(ObjectId())
        ))
    elif sign_type == 'appSign_once':
        path = request.args.get('path')
        sign = auth.sign_once('image', path)
        return json.dumps(dict(
            code="0", message='成功', data={'sign': sign}, key=str(ObjectId())
        ))
    else:
        return jsonify(code=10001, message='未指定签名方式')
