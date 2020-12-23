#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 11:14 上午
@des: 账号相关
"""
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection

from web.forms.account import RegisterModelForm, SendSmsForm


def send_sms(request):
    """发送验证码"""
    form = SendSmsForm(request, data=request.GET)

    if form.is_valid():
        JsonResponse({"status": True})

    return JsonResponse({"status": False})


def register(request):
    form = RegisterModelForm()
    return render(request, "register.html", {"form": form})
