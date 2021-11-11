# -*- encoding:utf-8 -*-
import datetime
import requests
import json
from urllib.parse import urlencode
from utils.dingdingBotUtil import DingDingBot


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
        # 实例化session
        self.session = requests.session()
        self.status_code = -1

    # 登陆
    def login(self):
        url = self.loginUrl + "?username=" + str(self.data['username']) + "&password=" + str(self.data['password'])
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
            self.status_code = 5
            return False

    # 设置JWSESSION
    def setJwsession(self, jwsession):
        self.header['JWSESSION'] = jwsession

    # 获取JWSESSION
    def getJwsession(self):
        return self.header['JWSESSION']

    # 测试登陆状态，若未登录或jwsession失效，请求返回code=-10
    def testLoginStatus(self):
        # 用任意需要鉴权的接口即可，这里随便选了一个
        url = "https://student.wozaixiaoyuan.com/heat/getTodayHeatList.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        if res['code'] == 0:
            # 已登陆
            return 1
        elif res['code'] == -10:
            # 未登录或jwsession失效
            self.status_code = 4
            return 0
        else:
            # 其他错误，打卡中止
            self.status_code = 0
            return -1

    # 获取打卡列表，判断当前打卡时间段与打卡情况，符合条件则自动进行打卡
    def PunchIn(self):
        url = "https://student.wozaixiaoyuan.com/heat/getTodayHeatList.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        # 遍历每个打卡时段（不同学校的打卡时段数量可能不一样）
        print(res) # test
        if res['code'] == 0:
            for i in res['data']:
                # 判断时段是否有效，一般情况下同一时刻只有一个有效时段
                if int(i['state']) == 1:
                    # 判断是否已经打卡
                    if int(i['type']) == 0:
                        self.doPunchIn(str(i['seq']))
                    elif int(i['type']) == 1:
                        print("已经打过卡了")
        elif res['code'] == -10:
            print("未登录或jwsession过期")
            self.status_code = 4
        else:
            print("未知错误")
            self.status_code = 0

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
            self.status_code = 1
        else:
            print("打卡失败")
            self.status_code = 0

    # 推送打卡结果
    def sendNotification(self):
        notify_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M')
        notify_result = self.getResult()
        # 如果开启了PushPlus
        if self.data['notification_type'] == "PushPlus":
            url = 'http://www.pushplus.plus/send'
            notify_token = self.data['notify_token']
            content = json.dumps({
                "打卡情况": notify_result,
                "打卡时间": notify_time
            }, ensure_ascii=False)
            msg = {
                "token": notify_token,
                "title": "⏰ 我在校园打卡结果通知",
                "content": content,
                "template": "json"
            }
            # 仅在失败情况下推送提醒
            if self.status_code != 1 and self.status_code != -1:
                requests.post(url, data=msg)
        elif self.data['notification_type'] == "DingDing":
            dingding = DingDingBot(self.data["dingding_access_token"],self.data['notify_token'])
            title = "⏰ 我在校园打卡结果通知"
            content = "## 我在校园打卡结果通知 \n" \
                      "打卡情况：{} \n \n " \
                      "打卡时间：{} \n".format(notify_result,notify_time)
            dingding.set_msg(title,content)
            # 仅在失败情况下推送提醒
            if self.status_code != 1 and self.status_code != -1:
                dingding.send()
        else:
            pass

    # 获取打卡结果
    def getResult(self):
        res = self.status_code
        if res == 1:
            return "✅ 打卡成功"
        elif res == 0:
            return "❌ 打卡失败，发生未知错误"
        elif res == 4:
            return "❌ 打卡失败，jwsession 失效"
        elif res == 5:
            return "❌ 打卡失败，登录错误，请检查账号信息"
        else:
            # 无事发生,不触发推送
            return "⭕"


