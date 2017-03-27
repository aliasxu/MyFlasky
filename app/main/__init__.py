#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import Blueprint

#实例化蓝本
main = Blueprint('main',__name__)

from . import views,errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)