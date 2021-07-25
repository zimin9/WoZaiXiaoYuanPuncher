import json
import os
import configparser
from .configHandler import ConfigReader


class Reader:
    def __init__(self):
        self.path = os.getcwd()

    def getJson(self, filename):
        with open(self.path + "/" + filename, 'r', encoding='utf8')as fp:
            json_data = json.load(fp)
            return json_data
