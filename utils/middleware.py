#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/24 10:18 上午
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse


class MD1(MiddlewareMixin):

    def process_request(self, request):
        print("md1  process_request 方法。", id(request))  # 在视图之前执行

    def process_response(self, request, response):
        # 基于请求响应
        print("md1  process_response 方法！", id(request))  # 在视图之后
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('process_view')

    def process_exception(self, request, exception):
        print('process_exception')
        return JsonResponse({'status': False, "error": exception[0]})
