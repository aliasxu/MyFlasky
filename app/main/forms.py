#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField
from wtforms.validators import Required,Length,Email,Regexp,ValidationError
from ..models import Role,User

class NameForm(FlaskForm):
    name = StringField('What is your name',validators=[Required()])
    submit = SubmitField('Submit')


#普通用户编辑用户资料表单类
class EditProfileForm(FlaskForm):
    name = StringField('Real Name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


#管理员编辑用户资料表单类
class EditProfileAdminForm(FlaskForm,object):
    email = StringField('Email',validators=[Length(0,64),Email()])
    username = StringField('Username',validators=[Length(0,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Username must be have letters,numbers,dots or underscores')])

    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me= TextAreaField('About me')
    submit = SubmitField('submit')

    def __init__(self,user,*args,**kwargs):
        super(EditProfileAdminForm,self).__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]

        self.user = user

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered!')


    def valudate_username(self,field):
        if field.data != self.user.username and  User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use')