# -*- encoding:utf-8 -*-
import datetime
from WoZaiXiaoYuanPuncher import WoZaiXiaoYuanPuncher
from utils.jsonHandler import JsonReader
from utils.sqlliteUtil import EasySqlite

# 以下是脚本相关配置，按实际情况修改。
# 填写SQLite的绝对路径，使用cron定时执行脚本时不要用相对路径！（找到项目根目录下的database.sqlite文件，复制其绝对路径）
SQLITE_DIR = "database.sqlite"
# 填写json文件的绝对路径
JSON_FILE = "source.json"

if __name__ == '__main__':
    json_util = JsonReader(JSON_FILE)
    json = json_util.getJson()
    connection = EasySqlite(SQLITE_DIR)
    for item in json:
        if item["jwsession"] == "None":
            try:
                result = connection.execute("select * from jwsession where username=?", [item["username"]])
                wzxy = WoZaiXiaoYuanPuncher(item)
                # 根据列表长度判断数据库中是否有该用户信息
                if len(result) > 0:
                    wzxy.setJwsession(result[0]["jwsession"])
                    login_status = wzxy.testLoginStatus()
                    if login_status == 1:
                        wzxy.PunchIn()
                    elif login_status == 0:
                        # 对于过期jwsession，重新登陆，若仍然失败会触发通知给用户（注意：一天只有5次登陆失败的机会，超过后账号会冻结24小时）
                        if wzxy.login():
                            # 获取新的jwsession存入数据库
                            connection.execute("update jwsession set jwsession = ? where username=?",[wzxy.getJwsession(),item["username"]])
                            wzxy.PunchIn()
                    else:
                        # 对于未知错误，仍然执行打卡，意图是触发失败通知给用户
                        wzxy.PunchIn()
                    # 根据结果发送通知
                    wzxy.sendNotification()
                else:
                    if wzxy.login():
                        wzxy.PunchIn()
                        connection.execute("insert into jwsession values (?,?,?,?)",[item["username"],
                                           wzxy.getJwsession(),datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M'),1])
                        wzxy.sendNotification()
            except:
                wzxy.status_code = 0
                wzxy.sendNotification()
        else:
            try:
                wzxy = WoZaiXiaoYuanPuncher(item)
                wzxy.setJwsession(item["jwsession"])
                login_status = wzxy.testLoginStatus()
                if login_status == 1:
                    wzxy.PunchIn()
                wzxy.sendNotification()
            except:
                wzxy.status_code = 0
                wzxy.sendNotification()