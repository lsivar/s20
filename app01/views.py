from django.shortcuts import render

# Create your views here.
from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django_redis import get_redis_connection


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
            field.widget.attrs['id'] = name
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label


def send_code(request):
    """发送验证码"""
    mobile_phone = request.GET.get("mobile_phone")
    conn = get_redis_connection('default')
    conn.set(mobile_phone, '111', ex=60)

    # 1.根据手机号码查询是否已失效
    print(conn.get(mobile_phone))
    # TODO 验证码完善
    return HttpResponse("OK")


def register(request):
    form = RegisterModelForm()
    return render(request, "app01/register.html", {"form": form})
