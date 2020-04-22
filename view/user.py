from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

bp = Blueprint('user', __name__, template_folder='templates')


@bp.route('/sign-in')
def sign_in():
    """"""


@bp.route('/sign-up')
def sign_up():
    """"""
