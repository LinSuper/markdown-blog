from flask import Flask, request, redirect, render_template
from gevent import monkey
monkey.patch_all()
from gevent.wsgi import WSGIServer
from api import api
from image import img
from flask.ext.login import LoginManager,login_required
from model.user import User
app = Flask(__name__)
app.debug = True
app.secret_key = 'dsafdggfivfngnkrhsgsas'
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(img, url_prefix='/img')
import user

@app.route('/')
#@login_required
def hello_world():
    return render_template('index.html')

@app.route('/test',methods=['POST'])
def get_list():
    import sys
    print>>sys.stderr,request.form
    return "get"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'http://localhost:9999/api/login'


@login_manager.user_loader
def load_user(user_id):
    user = User.p_col.find_one(user_id)
    return User(**user)

@login_manager.token_loader
def load_token(token):
    return User(**User.p_col.find_one({User.Field.token: token}))

# from werkzeug.serving import run_with_reloader
# @run_with_reloader
# def run_server():
#     http_server = WSGIServer(('0.0.0.0', 9999), app)
#     http_server.serve_forever()
app.run('0.0.0.0',port=9999)
