#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/22 11:19 下午
"""

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'

# 腾讯短信配置

TENCENT_SMS_APP_ID = 1400464016
TENCENT_SMS_SECRET_ID = 'AKID2uXwHO6UEk6E7lsKFvPktrdASXP18XR5'
TENCENT_SMS_SECRET_KEY = 'XqujJekbFiwvf9OO9kBPO9fvwkJcokQv'
TENCENT_SMS_SIGN = 'SG智能管理平台'

# django redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://119.29.147.199:12266/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 10,
                "encoding": "utf-8"
            },
            "PASSWORD": "FKJasd..SDF123..",
        }

    }
}