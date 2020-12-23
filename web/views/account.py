#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 11:14 上午
@des: 账号相关
"""
from django.http import JsonResponse
from django.shortcuts import render
import time
from web.forms.account import RegisterModelForm, SendSmsForm


def send_sms(request):
    """发送验证码"""
    form = SendSmsForm(request, data=request.GET)

    if form.is_valid():
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors})


def register(request):
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, "register.html", {"form": form})

    """注册"""
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 校验通过，存储数据
        # form.save自动剔除掉多余自动
        instance = form.save()
        return JsonResponse({"status": True, "data": "/login"})

    return JsonResponse({"status": False, "error": form.errors})
