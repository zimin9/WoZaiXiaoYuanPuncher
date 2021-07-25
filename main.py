# -*- encoding:utf-8 -*-
from WoZaiXiaoYuanPuncher import WoZaiXiaoYuanPuncher
from utils.configHandler import ConfigReader
from utils.jsonHandler import Reader


def getData(type):
    if type == "json":
        return readDataFromJson()


def readDataFromJson():
    json = Reader()
    return json.getJson(config.getJsonFileName())


if __name__ == '__main__':
    config = ConfigReader()
    data = getData(config.getDataSourceType())
    for item in data:
        wzxy = WoZaiXiaoYuanPuncher(item)
        loginStatus = wzxy.login()
        if loginStatus:
            wzxy.PunchIn()
        else:
            print("登陆失败")
