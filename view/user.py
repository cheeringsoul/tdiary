from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('account', __name__, url_prefix='/account')



class RegistrationForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='密码不匹配')
    ])
    confirm = PasswordField('repeat-password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


@bp.route('/login')
def login():
    if request.method == 'POST':
        form = RegistrationForm(request.form)
        if form.validate():
            user = User(form.username.data, form.email.data,
                        form.password.data)
            db_session.add(user)
            flash('Thanks for registering')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

