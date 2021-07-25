import os
import configparser


class ConfigReader:
    def __init__(self):
        root_dir = os.getcwd()  # 获取当前文件所在目录的上一级目录
        self.cf = configparser.ConfigParser()
        self.cf.read(root_dir + "/config.ini")  # 拼接得到config.ini文件的路径，直接使用

    def getDataSourceType(self):
        return self.cf.get("BasicConfig", "dataSourceType")

    def getJsonFileName(self):
        return self.cf.get("BasicConfig", "jsonFileName")
