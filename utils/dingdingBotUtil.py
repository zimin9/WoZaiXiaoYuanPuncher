# -*- encoding:utf-8 -*-
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests


class DingDingBot:
    def __init__(self,access_token,secret):
        # 秘钥
        self.secret = secret
        # token
        self.access_token = access_token
        self.data_dict = {
            "msgtype": "markdown",
            "markdown": {
                "title": "",
                "text": ""
            }
        }
        self.headers = {"Content-Type": "application/json"}

    def generate(self):
        self.timestamp = str(round(time.time() * 1000))
        self.secret_enc = self.secret.encode('utf-8')
        self.string_to_sign = '{}\n{}'.format(self.timestamp, self.secret)
        self.string_to_sign_enc = self.string_to_sign.encode('utf-8')
        self.hmac_code = hmac.new(self.secret_enc, self.string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = urllib.parse.quote_plus(base64.b64encode(self.hmac_code))

    def getSign(self):
        return self.sign

    def getTimestamp(self):
        return self.timestamp

    def getURL(self):
        url = 'https://oapi.dingtalk.com/robot/send?access_token=' + str(self.access_token)
        url = url + '&timestamp=' + self.timestamp + '&sign=' + self.sign
        return url

    # 设置发送的消息内容
    def set_msg(self, title, text):
        self.data_dict["markdown"]["title"] = title
        self.data_dict["markdown"]["text"] = text

    # 发送消息
    def send(self):
        self.generate()
        url = self.getURL()
        last_data = json.dumps(self.data_dict).encode("utf-8")
        result = requests.post(url, data=last_data, headers=self.headers)
        # 打印服务器端返回消息
        print(result.text)