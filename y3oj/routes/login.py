from flask_wtf import FlaskForm
from flask_login import login_required, login_user, logout_user
from wtforms import TextField, PasswordField, SubmitField
from flask import request, flash, abort, redirect, url_for

from y3oj import app
from y3oj.utils import render_template, is_safe_url
from y3oj.modules.user import get_user


@app.route('/login', methods=['GET', 'POST'])
def route_login():

    class LoginForm(FlaskForm):
        username = TextField('用户名')
        password = PasswordField('密码')
        submit = SubmitField('提交')

    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user is None:
            return render_template('login.html', form=form, snackbar_message='登录失败：用户不存在')

        if password != user.password:
            return render_template('login.html', form=form, snackbar_message='登录失败：用户名与密码不匹配')

        login_user(user)
        flash('Logged in successfully.')
        next = request.args.get('next')
        if not is_safe_url(request.host_url, next):
            return abort(400, 'Permission denied.')
        return redirect(next or url_for('route_index'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def route_logout():
    logout_user()
    return redirect(url_for('route_login'))
