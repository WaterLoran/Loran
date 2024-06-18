import os
import sys
from easydict import EasyDict as register
from core.context import ServiceContext


BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
print("BASE_PATH", BASE_PATH)

COMMON_PATH = os.path.join(BASE_PATH, 'common')
CONFIG_PATH = os.path.join(BASE_PATH, 'config')
FILES_PATH = os.path.join(BASE_PATH, 'files')
LOG_PATH = os.path.join(BASE_PATH, 'logs')
CORE_PATH = os.path.join(BASE_PATH, 'core')

# 将工程的基本的路径信息记录到业务上下文
service_context = ServiceContext()
service_context.base_path = BASE_PATH

sys.path.append(COMMON_PATH)
sys.path.append(CONFIG_PATH)
sys.path.append(CORE_PATH)

from core import hook
pytest_plugins = ["hook"]  # 导入并注册插件模块






