from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, sessions
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/login')
def login():
    session['name'] = 'ymy'
    return ""


@bp.route('/logout')
def logout():
    return session.pop('name')

