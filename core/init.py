import os
import sys
from easydict import EasyDict as register
from core.context import ServiceContext


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

sys.path.append(COMMON_PATH)
sys.path.append(CONFIG_PATH)

# 指定core目录, 因为打包成pip库之后, 工程的目录文件和core的目录文件就区分开了, 所以要以绝对路径的方式计算core的路径
core_base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CORE_PATH = os.path.join(core_base_path, 'core')
sys.path.append(CORE_PATH)
print("CORE_PATH", CORE_PATH)
sys.path.append(CORE_PATH)

from core import hook
from core.general_logic import *  # 导入通用logic, 即excel类的, 数据库操作类的logic
pytest_plugins = ["hook"]  # 导入并注册插件模块
