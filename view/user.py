from marshmallow import ValidationError
from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, abort, g
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_

from common.validate import RegisterSchema
from common.context import save_current_user
from ext import csrf
from model import User, Diary, Validated, open_db_session


bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'GET':
        return render_template('login.html')
    account = request.form.get('account', '').strip()   # todo 配置nginx最大传输限制
    password = request.form.get('password', '').strip()
    if not account:
        flash(f'账号不能为空,请用邮箱或用户名进行登录')
        return render_template('login.html')
    with open_db_session() as s:
        rv = s.query(User).filter(or_(User.name == account, User.email == account)).first()
        if not rv:
            flash(f'用户{account}不存在')
            return render_template('login.html')
        if not check_password_hash(rv.password, password):
            flash('密码不正确')
            return render_template('login.html')
    save_current_user({'id': rv.id, 'name': rv.name})
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
                flash('邮箱已经被注册')
                return render_template('signup.html')
            rv = db_session.query(User).filter_by(name=data['username']).first()
            if rv:
                flash('用户名已经被注册')
                return render_template('signup.html')
            user = User()
            user.name = data['username']
            user.email = data['email']
            user.validated = Validated.No
            user.password = generate_password_hash(data['password'])
            user.avatar = '/default_avatar.jpg'  # todo
            db_session.add(user)
            db_session.commit()

        flash('注册成功，请登录.')
        return redirect(url_for('account.login'))


@bp.route('/zone')
def zone():
    default_page_size = 3
    user_id = request.args.get('user_id', '')
    user_id = user_id.strip()
    page_no = request.args.get('page_no', '0')
    if not page_no.isdigit():
        # 恶意数据
        abort(404, description="Resource not found")
    page_no = int(page_no)
    if page_no < 0:
        # 恶意数据
        abort(404, description="Resource not found")
    with open_db_session() as db_session:
        user = db_session.query(User).get(user_id)
        if not user:
            abort(404, description="Resource not found")

        rv = db_session.query(Diary).order_by(Diary.created_at.desc()) \
            .limit(default_page_size).offset(page_no * default_page_size).all()
    if len(rv) == 0:

        flash("没有更多数据了!")

    if len(rv) < default_page_size:
        next_page = -1
    else:
        next_page = page_no + 1
    if page_no == 0:
        pre_page = -1
    else:
        pre_page = page_no - 1

    if g.current_user and int(user_id) == g.current_user['id']:
        # 当前登录用户查看自己个人空间
        private = 1
    else:
        # 访问他人空间
        private = 0
    return render_template('my_diary.html', diaries=rv, next_page=next_page, pre_page=pre_page,
                           avatar=user.avatar, user_id=user_id, private=private)
