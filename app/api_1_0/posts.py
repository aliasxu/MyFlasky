#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import  jsonify,request,g,abort,url_for,current_app
from .. import db
from ..models import Post,Permission
from . import api
from .decorators import permission_required
from .errors import forbidden

#查看所有文章/博客
@api.route('/posts/')
def get_posts():
    page =request.args.get('page',1,type=int)
    pagination = Post.query.paginate(page,
                                     per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts',page=page-1,_external=True)

    next = None
    if pagination.has_next:
        next = url_for('api.get_posts',page=page+1,_external=True)

    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev' : prev,
        'next' : next,
        'count' : pagination.total
    })


#查看指定的博客
@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())



#写博客
@api.route('/posts/',methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_json()),201,{'Location':url_for('api.get_post',id=post.id,_external=True)}


#修改博客
@api.route('/post/<int:id>',methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.from_json(request.json)
    if g.current_user != post.author and not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body',post.body)
    db.session.add(post)
    return jsonify(post.to_json())