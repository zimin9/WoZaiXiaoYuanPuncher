import json
import os
import configparser
from .configHandler import ConfigReader


class Reader:
    def __init__(self,path):
        self.path = path

    def getJson(self, filename):
        with open(self.path)as fp:
            json_data = json.load(fp)
            return json_data
