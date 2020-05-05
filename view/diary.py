from datetime import datetime
from marshmallow import ValidationError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, abort, url_for, current_app
)

from common.validate import DiarySchema
from ext import csrf
from model import open_db_session, Diary, DiaryType


bp = Blueprint('diary', __name__, url_prefix='/diary')


@bp.route('/')
def diary():
    default_page_size = 3
    page_no = request.args.get('page_no', '0')
    if not page_no.isdigit():
        # 恶意数据
        abort(404, description="Resource not found")
    page_no = int(page_no)
    if page_no < 0:
        # 恶意数据
        abort(404, description="Resource not found")
    with open_db_session() as db_session:
        rv = db_session.query(Diary).order_by(Diary.created_at.desc())\
            .limit(default_page_size).offset(page_no*default_page_size).all()
    if len(rv) == 0:
        flash("没有更多数据了!")
        return render_template('message.html', back=url_for('diary.diary'))
    if len(rv) < default_page_size:
        next_page = -1
    else:
        next_page = page_no + 1
    if page_no == 0:
        pre_page = -1
    else:
        pre_page = page_no - 1
    return render_template('index.html', diaries=rv, next_page=next_page, pre_page=pre_page)


@bp.route('/create', methods=['get', 'post'])
def create_diary():
    today = datetime.today()
    date = f"{today.year}年{today.month}月{today.day}日"
    if request.method == 'GET':
        return render_template('diary.html', date=date)
    diary_type = request.args.get('diary_type', 1)
    diary_type = int(diary_type)
    if diary_type not in (DiaryType.NewDiary, DiaryType.RewriteDiary, DiaryType.ContinueDiary):
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
        if d.diary_type == DiaryType.RewriteDiary:
            """"""
        elif d.diary_type == DiaryType.ContinueDiary:
            """"""
        with open_db_session() as db_session:
            db_session.add(d)
            db_session.commit()
        flash("发表成功.")
        return redirect(url_for('diary.create_diary', diary_type=diary_type))


@bp.route('/like', methods=['post'])
@csrf.exempt
def like():
    diary_id = request.form.get('id', None)
    if diary_id is None:
        current_app.logger.error('get empty diary id')
        return ""
    if g.current_user is None:
        """"""
    with open_db_session() as db_session:
        rv = db_session.query(Diary).get(diary_id)
        if not rv:
            current_app.logger.error(f'diary id {diary_id} not exists')
            return ""
        rv.like = rv.like + 1
        db_session.commit()
    return "success."




