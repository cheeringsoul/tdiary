from flask import Flask
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    """"""


@app.route('/sign-up')
def sign_up():
    """注册"""


@app.route('/sign-in')
def sign_in():
    """登陆"""


@app.route('/diary', methods=['POST'])
def post_diary():
    """发表日志"""


