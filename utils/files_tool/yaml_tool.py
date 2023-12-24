import os
import yaml


class YamlTool:
    def __init__(self, yaml_abs_path=""):
        self.path = yaml_abs_path

    def read_yaml_data(self):
        """
        读取yaml文件
        :return:
        """
        if os.path.exists(self.path):
            data = open(self.path, "r", encoding="utf-8")
            res = yaml.load(data, Loader=yaml.FullLoader)
        else:
            raise
        return res

    def update_yaml_data(self, **kwargs):
        pass
