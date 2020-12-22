from django.shortcuts import render

# Create your views here.
from django import forms
from app01 import models
from django.core.validators import RegexValidator


class RegisterModelForm(forms.ModelForm):
    """表单约束"""

    # 手机号正则表达式校验
    mobile_phone = forms.CharField(label="手机号", validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号码格式错误'), ])
    password = forms.CharField(label="密码", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)
    code = forms.CharField(label="验证码")

    class Meta:
        model = models.UserInfo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
        # TODO 已完成表单，继续

def register(request):
    form = RegisterModelForm()
    return render(request, "register.html", {"form": form})
