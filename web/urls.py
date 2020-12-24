"""s20 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from web.views import account, home

urlpatterns = [
    # namespace  app01:register
    path(r'index/', home.index, name='index'),
    path(r'logout/', account.logout, name='logout'),
    path(r'register/', account.register, name='register'),
    path(r'send/sms/', account.send_sms, name='send_sms'),
    path(r'login/sms/', account.login_sms, name='login_sms'),
    path(r'login/account/', account.login_account, name='login_account'),
    path(r'login/image/code/', account.image_code, name='image_code'),
]
