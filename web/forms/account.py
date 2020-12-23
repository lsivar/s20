#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 2:06 下午
"""
from django import forms
from django.core.validators import RegexValidator, ValidationError
from web import models
from django.conf import settings


class RegisterModelForm(forms.ModelForm):
    """表单约束"""

    # 手机号正则表达式校验
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误'), ])
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)
    code = forms.CharField(label="验证码")

    class Meta:
        model = models.UserInfo
        # 定义顺序
        fields = ['username', 'password', 'confirm_password', 'email', 'mobile_phone', 'code']
        # fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        # 校验手机号码是否存在
        if exists:
            raise ValidationError("手机号码已注册")
        # 校验短信模板是否存在
        tpl = self.request.GET.get('tpl')
        template_id = settings.SMS_TEMPLATES.get(tpl)
        if not template_id:
            raise ValidationError("短信模板不存在")

        # 发送短信

        # 存储Redis
        return mobile_phone
