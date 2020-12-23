#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 9:21 上午
"""

from django_redis import get_redis_connection

conn = get_redis_connection('default')
conn.set('11', '22', ex=50)
print(conn.get('11'))
