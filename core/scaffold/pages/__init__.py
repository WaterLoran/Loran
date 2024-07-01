# 导入seleniumbase的basecase, 用于给那个测试类继承, 以实现能够seleniumbase的效果
from core.init import *
from seleniumbase import BaseCase as RuoYiUicase


from .main_page import *
from .common_page import *
from .system_management_page import *
