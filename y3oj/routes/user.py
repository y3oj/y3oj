# -*- coding: UTF-8 -*-

from flask import g, abort, request
from wtforms import TextField, TextAreaField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import current_user, login_required

from y3oj import app, db, config
from y3oj.utils import render_template, to_mixin
from y3oj.modules.user import get_user
from y3oj.modules.submission import query_user_submissions
from y3oj.routes.decorater import user_checker


@app.route('/user/<id>')
@user_checker
def route_user(id):
    return render_template('user/user.html', user=g.user)


@app.route('/user/<id>/submission')
@user_checker
@login_required
def route_user_submission(id):
    if g.user != current_user and not current_user.has_root_authority:
        abort(400)

    pagination = query_user_submissions(g.user).paginate(
        page=int(request.args.get("page", 1)),
        per_page=int(config.per_page.submission))
    return render_template('user/submission.html',
                           user=g.user,
                           pagination=pagination,
                           submissions=map(to_mixin, pagination.items))


@app.route('/user/<id>/settings', methods=['GET', 'POST'])
@user_checker
@login_required
def route_user_settings(id):
    class UserSettingsForm(FlaskForm):
        summary = TextField('一句话简介')
        description = TextAreaField('关于我（支持 Markdown）')
        background_image = TextField('背景图片链接')
        old_password = PasswordField('旧密码')
        new_password = PasswordField('新密码')
        new_password_check = PasswordField('新密码（二次确认）')
        submit = SubmitField('提交')

    if g.user != current_user and not current_user.has_root_authority:
        abort(400)

    form = UserSettingsForm(
        summary=g.user.settings.get('summary'),
        description=g.user.settings.get('description'),
        background_image=g.user.settings.get('background_image'))

    if form.validate_on_submit():
        settings = g.user.settings

        if len(request.form['summary']) > config.user.limit.summary:
            return render_template(
                'user/settings.html',
                user=g.user,
                form=form,
                snackbar_message=f'「一句话简介」超出长度限制（{config.user.limit.summary}）')

        if len(request.form['description']) > config.user.limit.description:
            return render_template(
                'user/settings.html',
                user=g.user,
                form=form,
                snackbar_message=f'「关于我」超出长度限制（{config.user.limit.description}）'
            )

        if len(request.form['background_image']) > config.database.limit.link:
            return render_template('user/settings.html',
                                   user=g.user,
                                   form=form,
                                   snackbar_message=f'「背景图片链接」不合法')

        settings['summary'] = request.form['summary']
        settings['description'] = request.form['description']
        settings['background_image'] = request.form['background_image']

        if request.form['old_password'] and \
                request.form['new_password'] and \
                request.form['new_password_check']:
            oldpass = request.form['old_password']
            newpass = request.form['new_password']
            newpass_check = request.form['new_password_check']

            if oldpass != g.user.password:
                return render_template('user/settings.html',
                                       form=form,
                                       user=g.user,
                                       snackbar_message='密码错误')

            if newpass != newpass_check:
                return render_template('user/settings.html',
                                       form=form,
                                       user=g.user,
                                       snackbar_message='两次输入的密码不一致')

            g.user.password = newpass

        g.user.settings = settings
        db.session.add(g.user)

    return render_template('user/settings.html', form=form, user=g.user)
