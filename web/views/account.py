#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 11:14 上午
@des: 账号相关
"""
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
import time
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, AccountLoginForm
from web import models
from django.db.models import Q
from django.urls import reverse


def send_sms(request):
    """发送验证码"""
    form = SendSmsForm(request, data=request.GET)

    if form.is_valid():
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, "error": form.errors}, json_dumps_params={'ensure_ascii': False, })


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

    return JsonResponse({"status": False, "error": form.errors}, json_dumps_params={'ensure_ascii': False}, )


def login_sms(request):
    if request.method == "GET":
        form = LoginSMSForm()
        return render(request, "login_sms.html", {"form": form})

    # 登录校验
    form = LoginSMSForm(data=request.POST)
    if form.is_valid():
        # 登录成功,查询用户信息，存储session
        mobile_phone = form.cleaned_data['mobile_phone']
        user_info = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id'] = user_info.id
        request.session.set_expiry(60 * 60 * 24 * 14)
        return redirect('index')
    return JsonResponse({"status": False, "error": form.errors}, json_dumps_params={"ensure_ascii": False})


def login_account(request):
    """ 跳转登录页面 """
    if request.method == "GET":
        form = AccountLoginForm(request)
        return render(request, "login_account.html", {"form": form})

    """ 邮箱、手机号登录 """
    #  1.数据校验
    form = AccountLoginForm(request, data=request.POST)
    if form.is_valid():
        # 查询用户
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user_obj = models.UserInfo.objects.filter(
            Q(email=username) | Q(mobile_phone=username)).filter(password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('index') #TODO 完成页面跳转
        form.add_error("username", "邮箱、手机号或密码错误")
    return JsonResponse({"status": False, "error": form.errors})


def logout(request):
    """ 退出 """
    request.session.flush()
    return redirect('index')


def image_code(request):
    """ 生成登录验证码 """
    from utils.image_code import check_code
    from io import BytesIO

    image_object, code = check_code()
    stream = BytesIO()
    image_object.save(stream, 'png')

    request.session['image_code'] = code
    request.session.set_expiry(60)
    return HttpResponse(stream.getvalue())
