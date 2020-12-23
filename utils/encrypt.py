#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 10:33 下午
"""
import hashlib
from django.conf import settings


def md5(data):
    # 加盐
    hash_object = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    hash_object.update(data.encode("utf-8"))
    return hash_object.hexdigest()
