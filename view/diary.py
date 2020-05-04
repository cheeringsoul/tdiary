from datetime import datetime
from marshmallow import ValidationError
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ext import csrf
from common.validate import DiarySchema
from model import Session, Diary, DiaryType


bp = Blueprint('diary', __name__, url_prefix='/diary')


@bp.route('/')
def diary():
    return render_template('index.html')


@bp.route('/create', methods=['get', 'post'])
def create_diary():
    today = datetime.today()
    date = f"{today.year}年{today.month}月{today.day}日"
    if request.method == 'GET':
        return render_template('diary.html', date=date)
    try:
        data = DiarySchema().load(request.form)
    except ValidationError as e:
        for _, value in e.messages.items():
            flash(value[0])
    else:
        d = Diary()




