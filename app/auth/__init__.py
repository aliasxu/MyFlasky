#!/usr/bin/env python
#_*_ coding:utf-8 _*_

#创建认证蓝本
from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views