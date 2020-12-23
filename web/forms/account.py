#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 2:06 下午
"""
from django import forms
from django.core.validators import RegexValidator, ValidationError
from web import models
from utils.tencent import send_sms
import random
from django_redis import get_redis_connection
from django.conf import settings
from django.db.models import Q
import re
from utils.encrypt import *

class BootstarpForm(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label

class RegisterModelForm(BootstarpForm, forms.ModelForm):
    """表单约束
        注意：钩子获取数据是根据字段顺序赋值，校验顺序一定要按fields顺序
    """

    # 手机号正则表达式校验
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误'), ])

    # min_length=8, 这些约束会造成在钩子里面拿不到数据
    password = forms.CharField(label="密码",
                               min_length=8,
                               max_length=64,
                               error_messages={
                                   "min_length":"密码长度必须大于8位",
                                   "max_length":"密码长度不能大于64位"
                               },
                               widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)
    code = forms.CharField(label="验证码")

    class Meta:
        model = models.UserInfo
        # 定义顺序
        fields = ['username', 'password', 'confirm_password', 'email', 'mobile_phone', 'code']
        # fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 设置默认值
    #     self.fields['username'].initial="lsw"
    #     self.fields['email'].initial="290@qq.com"
    #     self.fields['mobile_phone'].initial="18818555102"
    #
    #     for name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = '请输入%s' % field.label

    def clean_username(self):
        # 2.账号、手机号是否已存在
        username = self.cleaned_data['username']
        if models.UserInfo.objects.filter(username=username).exists():
            raise ValidationError("账号已存在")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)

    def clean_confirm_password(self):
        # 3.密码是否一致
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != md5(confirm_password):
            raise ValidationError("密码不一致!")
        return confirm_password

    def clean_email(self):
        # 4.邮箱是否正确
        email = self.cleaned_data['email']
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email):
            raise ValidationError("邮箱格式错误")
        if models.UserInfo.objects.filter(email=email).exists():
            raise ValidationError("邮箱已存在!")
        return email

    def clean_mobile_phone(self):
        # 1.验证码
        conn = get_redis_connection()
        mobile_phone = self.cleaned_data['mobile_phone']
        if models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists():
            ValidationError("手机号已存在")
        return mobile_phone

    def clean_code(self):
        conn = get_redis_connection()
        code = self.cleaned_data['code']
        mobile_phone = self.cleaned_data['mobile_phone']
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码已失效，请重新发送")

        str_code = redis_code.decode('utf-8')
        if code.strip() != str_code:
            raise ValidationError("验证码错误!")
        return code

class LoginSMSForm(BootstarpForm, forms.Form):
    """ 短信登录 """
    mobile_phone = forms.CharField(label="手机号")
    code = forms.CharField(label="验证码")

    def clean_code(self):
        conn = get_redis_connection()
        mobile_phone = self.cleaned_data.get("mobile_phone")
        code = self.cleaned_data.get("code")
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError("验证码已失效，请重新发送")

        str_code = redis_code.decode('utf-8')
        if code.strip() != str_code:
            raise ValidationError("验证码错误!")
        return code

class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        conn = get_redis_connection()
        mobile_phone = self.cleaned_data['mobile_phone']
        # 1.校验Redis是否已有数据，提示禁止重复获取
        if conn.get(mobile_phone):
            raise ValidationError("60秒后才能重新发送")
        tpl = self.request.GET.get('tpl')
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()

        # 短信发送兼容
        if tpl == 'login':
            if not exists:
                raise ValidationError("手机号码不存在")
        else:
            # 校验手机号码是否存在
            if exists:
                raise ValidationError("手机号码已注册")
        # 校验短信模板是否存在

        template_id = settings.SMS_TEMPLATES_IDS.get(tpl)
        if not template_id:
            raise ValidationError("短信模板不存在")

        # 生产随机数
        code = random.randrange(1000, 9999)
        # 存储Redis

        conn.set(mobile_phone, code, ex=60)
        # 发送短信
        # send_sms.send_sms_single(mobile_phone, template_id, [str(code), ])
        return mobile_phone
