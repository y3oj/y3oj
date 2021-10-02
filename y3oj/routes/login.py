# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from flask_login import current_user, login_required, login_user, logout_user
from wtforms import TextField, PasswordField, SubmitField
from flask import request, flash, abort, redirect, url_for

from y3oj import app
from y3oj.utils import render_template, is_safe_url
from y3oj.modules.user import getUserById


class LoginForm(FlaskForm):
    username = TextField('用户名')
    password = PasswordField('密码')
    submit = SubmitField('提交')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('current_user', current_user)

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        user = getUserById(username).get_mixin()
        if password != user.password:
            return render_template('login.html', form=form, error='用户名与密码不匹配')

        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(request.host_url, next):
            return abort(400)
        return redirect(next or url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
