#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import render_template,session ,redirect,url_for,current_app,flash,request,abort
from .. import db
from ..models import User,Role,Post,Permission
from ..email import send_email
from . import main
from .forms import NameForm,EditProfileForm,EditProfileAdminForm,PostForm
from flask_login import login_required,current_user
from ..decorators import admin_required

@main.route('/', methods=['GET','POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #         if current_app.config['FLASKY_ADMIN']:
    #             send_email(current_app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
    #
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     return redirect(url_for('.index'))
    # return render_template('index.html',form = form ,name =session.get('name'),known = session.get('known',False))

    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        print type(current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    print posts
    return render_template('index.html',form=form,posts=posts,pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    print user.posts
    print type(user.posts)
    return render_template('user.html',user=user,posts=posts)


#普通用户修改用户资料视图函数
@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has benn updated')
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)


#管理员修改用户资料视图函数
@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm()
    if form.validate_on_submit():
        user.email= form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


#固定文章链接
@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html',posts=[post])

#编辑文章
@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated')
        return redirect(url_for('.post',id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html',form=form)