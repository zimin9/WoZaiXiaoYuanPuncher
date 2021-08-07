import json


class JsonReader:
    def __init__(self,path):
        self.path = path

    def getJson(self):
        with open(self.path, encoding='utf-8')as fp:
            json_data = json.load(fp)
            return json_data
