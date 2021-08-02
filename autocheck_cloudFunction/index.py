# -*- encoding:utf-8 -*-
import time
import datetime
import pytz
import requests
import json
from urllib.parse import urlencode


def get_status(status_code):
    if status_code == 1:
        return "打卡成功"
    elif status_code == 2:
        return "你已经打过卡了，无需重复打卡"
    elif status_code == 3:
        return "打卡失败，当前不在打卡时间段内"
    elif status_code == 4:
        return "打卡失败，登录错误，请检查账号信息"
    else:
        return "打卡失败，发生未知错误"

class WoZaiXiaoYuanPuncher:
    def __init__(self, item):
        # 我在校园账号数据
        self.data = item['wozaixiaoyaun_data']
        # 喵提醒账号数据
        self.miao_data = item['miao_data']
        # 打卡结果
        self.status_code = 0
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
            self.status_code = 4
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
        # 标志时段是否有效
        inPeriod = False
        # 遍历每个打卡时段（不同学校的打卡时段数量可能不一样）        
        for i in res['data']:
            # 判断时段是否有效
            if int(i['state']) == 1:
                inPeriod = True
                # 判断是否已经打卡
                if int(i['type']) == 0:
                    self.doPunchIn(str(i['seq']))
                elif int(i['type']) == 1:
                    self.status_code = 2
                    print("已经打过卡了")
        # 如果当前时间不在任何一个打卡时段内
        if inPeriod == False:            
            self.status_code = 3
            print("不在打卡时间段内")

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
            self.status_code = 1
            print("打卡成功")
        else:
            print("打卡失败")

    # 推送打卡结果
    def sendNotification(self):
        # 如果开启了消息推送
        if self.miao_data['isEnable'] == True:
            notifytoken = self.miao_data['notifytoken']
            notifyUser = self.miao_data['notifyUser']
            notifyTime = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
            notifyResult = get_status(self.status_code)
            msg = {
                "id": notifytoken,
                "text": '打卡人：' + notifyUser + '\n' + '打卡时间：' + notifyTime +  '\n' + '打卡情况：'  + notifyResult,
                "type": "json"
            }
            requests.post("http://miaotixing.com/trigger", data = msg)        

def main_handler(event, context):
   # 读取配置文件 
    with open("config.json",'rb') as json_file:
        configs = json.load(json_file)
    
    for config in configs:
        wzxy = WoZaiXiaoYuanPuncher(config)
        loginStatus = wzxy.login()
        if loginStatus:
            wzxy.PunchIn()
        else:
            print("登陆失败")        
        wzxy.sendNotification()    