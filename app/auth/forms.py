#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''
登录表单
'''

from flask_wtf import  FlaskForm
from wtforms import  StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

#登陆表单
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

#用户注册表单
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])
    password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must match')])

    password2 = PasswordField('Confirm password',validators=[Required()])

    submit = SubmitField('Register')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email arleady exists')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')


#修改密码
class ModifityPassword(FlaskForm):
    oldPassword = PasswordField('Old Password',validators=[Required()])
    newPassword = PasswordField('New Password',validators=[Required(),EqualTo('newPassword2',message='Password must match')])
    newPassword2 = PasswordField('Confirm password',validators=[Required()])
    submit = SubmitField('Change')




#重设密码
class ResetPasswordForm(FlaskForm):
    email = StringField('Please input your email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must match')])
    password2 = PasswordField('confirm password',validators=[Required()])
    submit = SubmitField('Reset')


    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')
