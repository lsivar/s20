#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/24 6:50 下午
"""
from django.utils.deprecation import MiddlewareMixin


class AutoMiddleware(MiddlewareMixin):
    """ 中间件，设置登录信息 """

    def process_request(self, request):
        user_id = request.session.get("user_id")
        print(user_id)
