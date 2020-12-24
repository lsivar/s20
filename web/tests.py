from django.test import TestCase

# Create your tests here.

# -*- coding: utf-8 -*-
from django.test import TestCase
from django_redis import get_redis_connection

from utils.encrypt import md5
class MyTestCase(TestCase):

    def md5test(self):
        data = 'lsw'
        print(md5(data))

    def testRedis(self):
        conn = get_redis_connection()
        conn.set('lsw', 345, ex=100)
        code = conn.get('lsw')
        print(code)
        print(code.decode('utf-8'))

    @classmethod
    def test(self):
        print("my is test")
