from marshmallow import ValidationError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

from common.validate import RegisterSchema
from ext import csrf
from model import User, Validated, open_db_session


bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'GET':
        return render_template('login.html')
    account = request.form.get('account', '').strip()   # todo 配置nginx最大传输限制
    password = request.form.get('password', '').strip()
    if not account:
        flash(f'账号不能为空,请用邮箱或用户名进行登陆')
        return render_template('login.html')
    with open_db_session() as s:
        rv = s.query(User).filter(or_(User.name == account, User.email == account)).first()
        if not rv:
            flash(f'用户{account}不存在')
            return render_template('login.html')
        if not check_password_hash(rv.password, password):
            flash('密码不正确')
            return render_template('login.html')
    session['current_user'] = {'id': rv.id, 'name': rv.name}

    return redirect(url_for('diary.diary'))


@bp.route('/logout')
def logout():
    if session.get('current_user'):
        session.pop('current_user')
    return redirect(url_for('diary.diary'))


@bp.route('/signup', methods=['get', 'post'])
@csrf.exempt
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    try:
        data = RegisterSchema().load(request.form)
    except ValidationError as e:
        for _, value in e.messages.items():
            flash(value[0])
            return render_template('signup.html')
    else:
        if data['password'] != data['password_repeated']:
            flash('两次密码不一致')
            return render_template('signup.html')
        with open_db_session() as db_session:
            rv = db_session.query(User).filter_by(email=data['email']).first()
            if rv:
                return '邮箱已经被注册'
            user = User()
            user.name = data['username']
            user.email = data['email']
            user.validated = Validated.No
            user.password = generate_password_hash(data['password'])
            user.avatar = '/default_avatar.jpg'  # todo
            db_session.add(user)
            db_session.commit()
        return render_template('signup.html')
