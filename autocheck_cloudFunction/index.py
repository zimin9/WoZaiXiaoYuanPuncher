# -*- encoding:utf-8 -*-
import requests
import json
import utils
from urllib.parse import urlencode
import leancloud


class _leanCloud:
    # 初始化 leanCloud 对象
    def __init__(self,appId,masterKey,objectId):
        leancloud.init(appId,master_key = masterKey)
        Jwsession = leancloud.Object.extend('Jwsession')
        self.obj = Jwsession.query.get(objectId)                
    # 获取 jwsession        
    def getJwsession(self):
        return self.obj.get('jwsession')
    # 设置 jwsession        
    def setJwsession(self,value):
        self.obj.set('jwsession',value)
        self.obj.save()

class WoZaiXiaoYuanPuncher:
    def __init__(self, item):
        # 我在校园账号数据
        self.data = item['wozaixiaoyaun_data']
        # pushPlus 账号数据
        self.pushPlus_data = item['pushPlus_data']
        # leanCloud 账号数据
        self.leanCloud_data = item['leanCloud_data']
        # 初始化 leanCloud 对象
        self.leanCloud_obj = _leanCloud(self.leanCloud_data['appId'],self.leanCloud_data['masterKey'],self.leanCloud_data['objectId'])
        # 学校打卡时段
        self.seqs = []
        # 打卡结果
        self.status_code = 0
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
        

    # 登录
    def login(self):
        # 登录接口
        loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        username,password = str(self.data['username']),str(self.data['password'])
        url = f'{loginUrl}?username={username}&password={password}'        
        self.session = requests.session()
        # 登录
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        if res["code"] == 0:
            print("登录成功")
            jwsession = response.headers['JWSESSION']
            self.leanCloud_obj.setJwsession(jwsession)
            return True
        else:
            print("登录失败，请检查账号信息")
            self.status_code = 5
            return False

    # 获取打卡列表，判断当前打卡时间段与打卡情况，符合条件则自动进行打卡
    def PunchIn(self):
        url = "https://student.wozaixiaoyuan.com/heat/getTodayHeatList.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        self.header['JWSESSION'] = self.leanCloud_obj.getJwsession() 
        self.session = requests.session() 
        response = self.session.post(url = url, data = self.body, headers = self.header)
        res = json.loads(response.text)
        # 如果 jwsession 无效，则重新 登录 + 打卡
        if res['code'] == -10:
            print('jwsession 无效')
            self.status_code = 4
            loginStatus = self.login()
            if loginStatus:
                print("登录成功")
                self.PunchIn()
            else:
                print("登录失败")    
        elif res['code'] == 0:            
            # 标志时段是否有效
            inSeq = False
            # 遍历每个打卡时段（不同学校的打卡时段数量可能不一样）        
            for i in res['data']:
                # 保存当前学校的打卡时段
                self.seqs.append({
                    's': int(i['startTime'][0:2]),
                    'e': int(i['endTime'][0:2])
                })
                # 判断时段是否有效
                if int(i['state']) == 1:
                    inSeq = True
                    # 判断是否已经打卡
                    if int(i['type']) == 0:
                        self.doPunchIn(str(i['seq']))
                    elif int(i['type']) == 1:
                        self.status_code = 2
                        print("已经打过卡了")
            # 如果当前时间不在任何一个打卡时段内
            if inSeq == False:            
                self.status_code = 3
                print("不在打卡时间段内")
    
    # 执行打卡
    # 参数seq ： 当前打卡的序号
    def doPunchIn(self, seq):
        url = "https://student.wozaixiaoyuan.com/heat/save.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        self.header['Content-Type'] = "application/x-www-form-urlencoded"
        sign_data = {
            "answers": '["0"]',
            "seq": str(seq),
            "temperature": utils.getRandomTemprature(self.data['temperature']),
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
    
    # 获取打卡时段
    def getSeq(self):
        seqs = self.seqs
        if len(seqs) == 0:
            seqs = [
                {'s':0,'e':9},
                {'s':11,'e':15},
                {'s':17,'e':23}
            ]
        current_hour = utils.getCurrentHour()
        if seqs[0]['s'] <= current_hour <= seqs[0]['e']:
            return "早打卡"
        elif seqs[1]['s'] <= current_hour < seqs[1]['e']:
            return "午打卡"
        elif seqs[2]['s'] <= current_hour < seqs[2]['e']:
            return "晚打卡"
        else:
            return "非打卡时段"
    
    # 获取打卡结果
    def getResult(self):
        res = self.status_code
        if res == 1:
            return "✅ 打卡成功"
        elif res == 2:
            return "✅ 你已经打过卡了，无需重复打卡"
        elif res == 3:
            return "❌ 打卡失败，当前不在打卡时间段内"
        elif res == 4:
            return "❌ 打卡失败，jwsession 无效"            
        elif res == 5:
            return "❌ 打卡失败，登录错误，请检查账号信息"
        else:
            return "❌ 打卡失败，发生未知错误"
    
    # 推送打卡结果
    def sendNotification(self):
        # 如果开启了消息推送
        if self.pushPlus_data['isEnable'] == True:
            url = 'http://www.pushplus.plus/send'
            notifyToken = self.pushPlus_data['notifyToken']
            notifySeq = self.getSeq()
            notifyTime = utils.getCurrentTime()
            notifyResult = self.getResult()
            
            content = json.dumps({
                "打卡情况": notifyResult,
                "打卡时段": notifySeq,
                "打卡时间": notifyTime
            },ensure_ascii = False)

            msg = {
                "token": notifyToken,
                "title": "⏰ 我在校园打卡结果通知",
                "content": content,
                "template": "json"
            }
            requests.post(url, data = msg)        

def main_handler(event, context):
    # 读取配置文件 
    configs = utils.processJson("config.json").read()
    # 遍历每个用户的账户数据，进行打卡  
    for config in configs:
        wzxy = WoZaiXiaoYuanPuncher(config)
        jwsession = wzxy.leanCloud_obj.getJwsession()
        # 如果没有 jwsession，则 登录 + 打卡
        if jwsession == "" or jwsession is None:
            loginStatus = wzxy.login()
            if loginStatus:
                print("登录成功")
                wzxy.PunchIn()
            else:
                print("登录失败")    
        # 如果有 jwsession，则直接打卡
        else:            
            wzxy.PunchIn()
        wzxy.sendNotification()    