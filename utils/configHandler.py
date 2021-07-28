import os
import configparser


class ConfigReader:
    def __init__(self,path):
        self.cf = configparser.ConfigParser()
        self.cf.read(path)

    def getDataSourceType(self):
        return self.cf.get("BasicConfig", "dataSourceType")
