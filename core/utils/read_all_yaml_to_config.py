import os
from core.utils.files_tool.yaml_tool import YamlTool
from easydict import EasyDict
from core.context import ServiceContext

def load_all_config_base_config_path(config_path=""):
    try:
        service_context = ServiceContext()
        if config_path != "":  # 用于调试场景, 手工传入配置的路径  XX\config
            CONFIG_PATH = config_path
        else:
            CONFIG_PATH = service_context.config_path

        config = {}
        # 查找出当前目录下的所有yaml文件
        # 然后都一次读出来, 然后update追加到config中
        files_list = os.listdir(CONFIG_PATH)
        for yaml_file in files_list:
            if yaml_file.endswith("yaml") or yaml_file.endswith("yml"):
                cur_yaml = os.path.join(CONFIG_PATH, yaml_file)
                cur_config = YamlTool(yaml_abs_path=cur_yaml).read_yaml_data()
                # TODO, 这里以后更新数据进去的时候, 要校验一下, 数据是否重复, 如果有的话, 就要抛出异常信息, 并说明定位信息
                config.update(cur_config)

        config = EasyDict(config)

    except:
        print("读取yaml文件信息出错")
        raise
    return config
