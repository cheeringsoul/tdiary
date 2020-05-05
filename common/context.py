from flask import session, g


def load_current_user():
    g.current_user = session.get('current_user', None)


def save_current_user(user_info):
    session['current_user'] = user_info
