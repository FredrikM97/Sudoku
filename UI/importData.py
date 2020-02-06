import json

class Json_handler:
    def __init__(self, PATH=None):
        self.path = PATH
        self.data = self.openConfig()

    def openConfig(self):
        with open(self.path) as json_data_file:
            data = json.load(json_data_file)
            return data
    def saveConfig(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.data, outfile, ensure_ascii=False, indent=4)
    