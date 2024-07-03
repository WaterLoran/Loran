import os
import sys
from easydict import EasyDict as register
from loran.context import ServiceContext


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   初始化各类目录
def get_project_root():
    for path in sys.path:
        if os.path.exists(os.path.join(path, 'cases')) or os.path.exists(os.path.join(path, 'case')):  # 包含cases的, 就是根目录
            return os.path.abspath(path)
    raise FileNotFoundError("Could not find project root containing setup.py")


BASE_PATH = get_project_root()

print("BASE_PATH", BASE_PATH)

COMMON_PATH = os.path.join(BASE_PATH, 'common')
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
FILES_PATH = os.path.join(BASE_PATH, 'files')
LOG_PATH = os.path.join(BASE_PATH, 'logs')

# 将工程的基本的路径信息记录到业务上下文
service_context = ServiceContext()
service_context.base_path = BASE_PATH
service_context.log_path = LOG_PATH
service_context.config_path = CONFIG_PATH


# 指定core目录, 因为打包成pip库之后, 工程的目录文件和core的目录文件就区分开了, 所以要以绝对路径的方式计算core的路径
core_base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CORE_PATH = os.path.join(core_base_path, 'loran')
sys.path.append(CORE_PATH)

sys.path.append(COMMON_PATH)
sys.path.append(CONFIG_PATH)
sys.path.append(CORE_PATH)
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 初始化各类目录


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 初始化pytest钩子函数
from loran import hook
pytest_plugins = ["hook"]  # 导入并注册插件模块
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 初始化pytest钩子函数

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 初始化config中的所有配置
from loran.utils.read_all_yaml_to_config import load_all_config_base_config_path
config = load_all_config_base_config_path()
service_context.config = config
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 初始化config中的所有配置

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 导入通用logic
from loran.general_logic import *  # 导入通用logic, 即excel类的, 数据库操作类的logic
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 导入通用logic