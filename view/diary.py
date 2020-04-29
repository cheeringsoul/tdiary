from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('diary', __name__, url_prefix='/diary')


@bp.route('/')
def diary():
    return render_template('index.html')


@bp.route('/create')
def create_diary():
    if request.method == 'GET':
        return render_template('diary.html')
    elif request.method == 'POST':
        return ""
