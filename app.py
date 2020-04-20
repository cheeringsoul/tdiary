from flask import Flask


app = Flask(__name__)


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


