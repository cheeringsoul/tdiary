from datetime import datetime, timedelta
from marshmallow import ValidationError
from flask import (
    Blueprint, flash, g, redirect, render_template,
    url_for, current_app, session, request, abort
)

from common.validate import DiarySchema
from ext import csrf
from model import open_db_session, Diary, DiaryType, Like, User


bp = Blueprint('diary', __name__, url_prefix='/diary')
default_img = 'noimage.png'


@bp.route('/')
def get_diary():
    default_page_size = 30
    page_no = request.args.get('page_no', '0')
    if not page_no.isdigit():
        # 恶意数据
        abort(404, description="Resource not found")
    page_no = int(page_no)
    if page_no < 0:
        # 恶意数据
        abort(404, description="Resource not found")
    result = []
    with open_db_session() as db_session:
        rv = db_session.query(Diary, User).join(User, Diary.creator_id == User.id, isouter=True)\
            .filter(Diary.diary_type == DiaryType.NewDiary).order_by(Diary.created_at.desc(), Diary.like.desc()) \
            .limit(default_page_size).offset(page_no * default_page_size).all()
        for each in rv:
            diary, user = each
            if diary:
                result.append({
                    'created_at': diary.created_at,
                    'weather': diary.weather,
                    'content': diary.content,
                    'diary_id': diary.id,
                    'like': diary.like,
                    'rewrite': diary.rewrite if diary.rewrite else '',
                    'username': user.name if user else "匿名用户",
                    "user_id": user.id if user else "",
                    'avatar': user.avatar if user else default_img
                })
    if len(rv) == 0:
        flash("没有更多数据了!")
        return render_template('message.html', back=url_for('diary.get_diary'))
    if len(rv) < default_page_size:
        next_page = -1
    else:
        next_page = page_no + 1
    if page_no == 0:
        pre_page = -1
    else:
        pre_page = page_no - 1
    return render_template("index.html", diaries=result, next_page=next_page, pre_page=pre_page)


@bp.route('/create', methods=['get', 'post'])
def create_diary():
    diary_type = request.args.get('diary_type', 1)
    diary_type = int(diary_type)
    parent_diary_id = request.args.get('diary_id', None)
    today = f"{datetime.today().year}年{datetime.today().month}月{datetime.today().day}日"
    if request.method == 'GET':
        result = []
        second_day, third_day = '', ''
        if diary_type == DiaryType.ContinueDiary and parent_diary_id:
            with open_db_session() as db_session:
                rv = db_session.query(Diary, User).join(User, Diary.creator_id == User.id, isouter=True) \
                    .filter(Diary.parent_id == parent_diary_id).order_by(Diary.created_at.asc(), Diary.like.desc()).all()
                for each in rv:
                    diary, user = each
                    if diary:
                        result.append({
                            'created_at': diary.created_at,
                            'weather': diary.weather,
                            'content': diary.content,
                            'diary_id': diary.id,
                            'like': diary.like,
                            'username': user.name if user else "匿名用户",
                            "user_id": user.id if user else "",
                            'avatar': user.avatar if user else default_img
                        })
                rv = db_session.query(Diary, User).join(User, Diary.creator_id == User.id, isouter=True) \
                    .filter(Diary.id == parent_diary_id).first()
                parent_diary, parent_diary_user = rv
                second_day, third_day = parent_diary.created_at+timedelta(days=1), parent_diary.created_at+timedelta(days=2)
                parent_diary_content = {
                    'created_at': parent_diary.created_at,
                    'weather': parent_diary.weather,
                    'content': parent_diary.content,
                    'diary_id': parent_diary.id,
                    'like': parent_diary.like,
                    'username': parent_diary_user.name if parent_diary_user else "匿名用户",
                    "user_id": parent_diary_user.id if parent_diary_user else "",
                    'avatar': parent_diary_user.avatar if parent_diary_user else default_img
                }
                result.insert(0, parent_diary_content)
        return render_template('diary.html', diary_type=diary_type, today=today, today_date=datetime.today(),
                               diaries=result, second_day=second_day, third_day=third_day, parent_diary=parent_diary)

    if diary_type not in (DiaryType.NewDiary, DiaryType.ContinueDiary):
        current_app.logger.error(f'wrong diary type {diary_type}')
        return ""
    try:
        data = DiarySchema().load(request.form)
    except ValidationError as e:
        for _, value in e.messages.items():
            flash(value[0])
            return redirect(url_for('diary.create_diary', diary_type=diary_type))
    else:
        d = Diary()
        d.content = data['diary_content']
        d.weather = data['weather']
        if g.current_user:
            d.creator_id = g.current_user['id']
        d.diary_type = diary_type
        try:
            with open_db_session() as db_session:
                if d.diary_type == DiaryType.ContinueDiary and parent_diary_id:
                    d.parent_id = parent_diary_id
                    parent_diary = db_session.query(Diary).get(parent_diary_id)
                    parent_diary.rewrite += 1
                    if data['date'] == 'N':
                        d.created_at = parent_diary.created_at + timedelta(days=3)  # N天后
                    else:
                        d.created_at = data['date']
                db_session.add(d)
                db_session.commit()
        except Exception as e:
            current_app.logger.error(e)
            flash("服务器异常!")
        else:
            flash("发表成功.")
        return render_template("message.html")


@bp.route('/like', methods=['post'])
@csrf.exempt
def like():
    diary_id = request.form.get('id', None)
    if not diary_id:
        current_app.logger.error('get empty diary id')
        return ""
    with open_db_session() as db_session:
        rv = db_session.query(Diary).get(diary_id)
        if not rv:
            current_app.logger.error(f'diary id {diary_id} not exists')
            return ""
        if not g.current_user:
            # 未登陆用户在cookie中标记liked，防止重复点赞
            rv.like = rv.like + 1
        else:
            user_id = g.current_user['id']
            liked = db_session.query(Like).filter_by(user_id=user_id).filter_by(diary_id=diary_id).first()
            if not liked:
                li = Like()
                li.user_id = g.current_user['id']
                li.diary_id = diary_id
                db_session.add(li)
                rv.like = rv.like + 1
        db_session.commit()
    return "success."
