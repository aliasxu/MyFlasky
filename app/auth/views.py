#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import render_template,redirect,request,url_for,flash,current_app
from flask_login import login_user,logout_user,login_required,current_user
from . import auth
from .forms import LoginForm,RegistrationForm,ModifityPassword,ResetPasswordForm
from ..models import User
from .. import db
from ..email import send_email

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')



#登陆函数
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            #用户名不为空且密码匹配正确
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')

    return render_template('auth/login.html',form=form)

#登出函数
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))


#注册函数
@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,'Confirm Your Account','/auth/email/confirm',user=user,token=token)
        flash('A confirmation email has been sent to you email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)


#确认账户
@auth.route('/confirm/<token>')
@login_required
def confirm(token):

    if current_user.confirmed:
        # print current_user
        # print type(current_user)
        # print current_user.id
        # print current_app.config
        #如果用户已经验证，直接重定向到首页
        return redirect(url_for('main.index'))
    #判断token
    if current_user.confirm(token):
        flash('You have confirmed your account.Thanks!')
    else:
        flash('The confirmation link is invalid or has expried')

    return redirect(url_for('main.index'))


#再次发送确认账户邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

#修改密码
@auth.route('/modifityPassword',methods=['GET','POST'])
@login_required
def modifityPassword():
    form = ModifityPassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldPassword.data):
            current_user.password = form.newPassword.data
            db.session.add(current_user)
            flash('Change password is success!')
            return  redirect(url_for('main.index'))
        else:
            flash('Invalid password')
    return render_template('auth/modifitypassword.html',form=form)


#重置密码
@auth.route('/reset',methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email,'Reset Your Password','auth/email/reset_password',user=user,token=token,next=request.args.get('next'))

        flash('An email with instructions to reset your password has been sent to you')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)

@auth.route('/reset/<token>',methods=['GET','POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token,form.password.data):
            flash('Your password has ben updated')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html',form=form)