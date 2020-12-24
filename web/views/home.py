#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/24 5:28 下午
"""
from django.shortcuts import render


def index(request):
    return render(request, "index.html")
