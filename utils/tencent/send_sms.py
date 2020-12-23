#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: LSW
@time: 2020/12/23 4:20 下午
"""
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入 SMS 模块的client models
from tencentcloud.sms.v20190711 import sms_client, models

# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from django.core.validators import ValidationError

'''
{
  "SendStatusSet": [
    {
      "SerialNo": "2019:-3764701951247844923",
      "PhoneNumber": "+8618818555102",
      "Fee": 1,
      "SessionContext": "",
      "Code": "Ok",
      "Message": "send success",
      "IsoCode": "CN"
    }
  ],
  "RequestId": "55c8e709-92c9-4af3-9f0e-776d2568fe42"
}
'''
from django.conf import settings


def send_sms_single(phone_num, template_id, template_param_list):
    """
    发送短信
    :param phone_num:           手机号码
    :param template_id:         模板ID
    :param template_param_list:  模板内容
    """
    try:
        secretId = settings.TENCENT_SMS_SECRET_ID
        secretKey = settings.TENCENT_SMS_SECRET_KEY
        appid = settings.TENCENT_SMS_APP_ID
        sign = settings.TENCENT_SMS_SIGN
        cred = credential.Credential(secretId, secretKey)
        httpProfile = HttpProfile()
        httpProfile.reqMethod = "POST"  # POST 请求（默认为 POST 请求）
        httpProfile.reqTimeout = 30  # 请求超时时间，单位为秒（默认60秒）
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名（默认就近接入）

        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile

        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
        req = models.SendSmsRequest()

        req.SmsSdkAppid = appid
        # 短信签名内容: 使用 UTF-8 编码，必须填写已审核通过的签名，可登录 [短信控制台] 查看签名信息
        req.Sign = sign
        # 短信码号扩展号: 默认未开通，如需开通请联系 [sms helper]
        req.ExtendCode = ""
        # 用户的 session 内容: 可以携带用户侧 ID 等上下文信息，server 会原样返回
        req.SessionContext = ""
        # 国际/港澳台短信 senderid: 国内短信填空，默认未开通，如需开通请联系 [sms helper]
        req.SenderId = ""
        # 下发手机号码，采用 e.164 标准，+[国家或地区码][手机号]
        # 例如+8613711112222， 其中前面有一个+号 ，86为国家码，13711112222为手机号，最多不要超过200个手机号
        phone_num = "+86{}".format(phone_num)
        req.PhoneNumberSet = [phone_num]
        # 模板 ID: 必须填写已审核通过的模板 ID，可登录 [短信控制台] 查看模板 ID
        req.TemplateID = template_id
        # 模板参数: 若无模板参数，则设置为空
        req.TemplateParamSet = template_param_list

        # 通过 client 对象调用 SendSms 方法发起请求。注意请求方法名与请求对象是对应的
        resp = client.SendSms(req)

        # 输出 JSON 格式的字符串回包
        print(resp.to_json_string(indent=2))

    except TencentCloudSDKException as err:
        print(err)
        raise ValidationError("短信发送失败!")
