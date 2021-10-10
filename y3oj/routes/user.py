# -*- coding: UTF-8 -*-

from flask import g, abort, request
from wtforms import TextAreaField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import current_user, login_required

from y3oj import app, db
from y3oj.utils import render_template
from y3oj.models import User
from y3oj.routes.decorater import user_checker


@app.route('/user/<id>')
@user_checker
def route_user(id):
    return render_template('user/user.html', user=g.user)


@app.route('/user/<id>/settings', methods=['GET', 'POST'])
@user_checker
@login_required
def route_user_settings(id):
    class UserSettingsForm(FlaskForm):
        summary = TextAreaField('个人简介')
        old_password = PasswordField('旧密码')
        new_password = PasswordField('新密码')
        new_password_check = PasswordField('新密码（二次确认）')
        submit = SubmitField('提交')

    if g.user != current_user:
        abort(400)

    form = UserSettingsForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(key=current_user.key).first()

        if request.form['old_password']:
            oldpass = request.form['old_password']
            newpass = request.form['new_password']
            newpass_check = request.form['new_password_check']

            if oldpass != current_user.password:
                return render_template('user/settings.html',
                                       form=form,
                                       snackbar_error='密码错误')

            if newpass != newpass_check:
                return render_template('user/settings.html',
                                       form=form,
                                       snackbar_error='两次输入的密码不一致')

            print('changepassword', current_user.id, oldpass, newpass)
            user.password = newpass

        user.settings['summary'] = request.form['summary']
        print(user)
        db.session.add(user)

    return render_template('user/settings.html', form=form)
