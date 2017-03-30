#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import  Blueprint

api = Blueprint('api',__name__)

from . import authentication,comments,decorators,errors,posts,users
