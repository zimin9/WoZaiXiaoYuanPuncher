# -*- encoding:utf-8 -*-
import time
import requests
import json
from urllib.parse import urlencode


class WoZaiXiaoYuanPuncher:
    def __init__(self, item):
        # 账号数据
        self.data = item
        # 登陆接口
        self.loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        # 请求头
        self.header = {
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Content-Type": "application/json;charset=UTF-8",
            "Content-Length": "2",
            "Host": "gw.wozaixiaoyuan.com",
            "Accept-Language": "en-us,en",
            "Accept": "application/json, text/plain, */*"
        }
        # 请求体（必须有）
        self.body = "{}"

    # 登陆
    def login(self):
        url = self.loginUrl + "?username=" + str(self.data['username']) + "&password=" + str(self.data['password'])
        self.session = requests.session()
        # 登陆
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        if res["code"] == 0:
            print("登陆成功")
            jwsession = response.headers['JWSESSION']
            self.setJwsession(jwsession)
            return True
        else:
            print("登陆失败，请检查账号信息")
            return False

    # 设置JWSESSION
    def setJwsession(self, jwsession):
        self.header['JWSESSION'] = jwsession

    # 获取打卡列表，判断当前打卡时间段与打卡情况，符合条件则自动进行打卡
    def PunchIn(self):
        url = "https://student.wozaixiaoyuan.com/heat/getTodayHeatList.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        # 遍历每个打卡时段（不同学校的打卡时段数量可能不一样）
        for i in res['data']:
            # 判断时段是否有效
            if int(i['state']) == 1:
                # 判断是否已经打卡
                if int(i['type']) == 0:
                    self.doPunchIn(str(i['seq']))
                elif int(i['type']) == 1:
                    print("已经打过卡了")

    # 执行打卡
    # 参数seq ： 当前打卡的序号
    def doPunchIn(self, seq):
        self.header['Host'] = "student.wozaixiaoyuan.com"
        self.header['Content-Type'] = "application/x-www-form-urlencoded"
        url = "https://student.wozaixiaoyuan.com/heat/save.json"
        sign_data = {
            "answers": '["0"]',
            "seq": str(seq),
            "temperature": self.data['temperature'],
            "latitude": self.data['latitude'],
            "longitude": self.data['longitude'],
            "country": self.data['country'],
            "city": self.data['city'],
            "district": self.data['district'],
            "province": self.data['province'],
            "township": self.data['township'],
            "street": self.data['street'],
            "myArea": self.data['myArea'],
            "areacode": self.data['areacode'],
            "userId": self.data['userId']
        }
        data = urlencode(sign_data)
        response = self.session.post(url=url, data=data, headers=self.header)
        response = json.loads(response.text)
        # 打卡情况
        if response["code"] == 0:
            print("打卡成功")
        else:
            print("打卡失败")

