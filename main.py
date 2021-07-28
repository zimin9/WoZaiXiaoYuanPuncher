# -*- encoding:utf-8 -*-
from WoZaiXiaoYuanPuncher import WoZaiXiaoYuanPuncher
from utils.configHandler import ConfigReader
from utils.jsonHandler import Reader


def getData(type):
    if type == "json":
        return readDataFromJson()


def readDataFromJson():
    json = Reader(json_path)
    return json.getJson()


if __name__ == '__main__':
    # 填入配置文件所在路径
    config_path = "C:\\Users\\xxxx\\Desktop\\WoZaiXiaoYuanPuncher\\config.ini"
    # 填入json文件所在路径
    json_path = "C:\\Users\\xxxx\\Desktop\\WoZaiXiaoYuanPuncher\\source.json"
    config = ConfigReader(config_path)
    data = getData(config.getDataSourceType())
    for item in data:
        wzxy = WoZaiXiaoYuanPuncher(item)
        loginStatus = wzxy.login()
        if loginStatus:
            wzxy.PunchIn()
        else:
            print("登陆失败")
