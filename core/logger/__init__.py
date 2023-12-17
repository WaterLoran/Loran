import os
import time
import logging
import logging.handlers
import colorlog
from core.init import LOG_PATH


class SingletonMeta(type):
    """
    功能: 实现一个单例模式的基类,只要子类集成这个类即可实现单例模式
    目的: 解决日志管理器在多处调用都能保证是同一个
    TODO 该单例模式可能存在线程不安全的问题,如果在实际使用中,出现该问题,可重新修改代码,参考连接如下
    https://refactoringguru.cn/design-patterns/singleton/python/example#example-0

    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class LoggerManager(metaclass=SingletonMeta):
    def __init__(self):
        self.file_handler = None
        self.stream_handler = None
        pass

    def get_log_file_name(self, case_file_path):
        # 输入源     E:\Develop\RuoYiTest\cases\api\system_management\user_management\test_add_user_998.py
        # 目标输出:  E:\Develop\RuoYiTest\logs\api\system_management\user_management\test_add_user_998.log
        # 加上时间戳:  E:\Develop\RuoYiTest\logs\api\system_management\user_management\test_add_user_998_20231213212138.log
        # 加上时间戳:  E:\Develop\RuoYiTest\logs\api\system_management\user_management\test_add_user_998\test_add_user_998_20231213212138.log
        pass

        # 获取文件名, 比如  test_add_user

        py_file_name = os.path.split(case_file_path)[1]
        py_file_name = py_file_name.strip(".py")
        # print("py_file_name", py_file_name)

        # 获取时间戳后缀,
        current = time.localtime()
        time_suffix = "_%d_%d_%d_%d_%d_%d" % (
            current.tm_year, current.tm_mon, current.tm_mday,
            current.tm_hour, current.tm_min, current.tm_sec
        )

        # 根据用例文件,获取相对路径信息
        new_folder_list = []
        new_folder_list.append(py_file_name)          #  预计为  ["test_add_user"]
        file_path = os.path.split(case_file_path)[0]  # E:\Develop\RuoYiTest\cases\api\system_management\user_management

        cur_folder = ""
        while cur_folder != "cases":
            path_detail = os.path.split(file_path)
            file_path = path_detail[0]
            cur_folder = path_detail[1]
            new_folder_list.append(cur_folder)
        new_folder_list = new_folder_list[::-1]   #  ["test_add_user", "user_management", "system_management", "api"]

        # print("new_folder_list", new_folder_list)
        t_folder = "cases"  # 用例文件的相对路径, 即根据用例的相对路径,去记录一些路径信息,将用于生存路径
        for i in range(1, len(new_folder_list)):
            t_folder = os.path.join(t_folder, new_folder_list[i])

        # 生成日志文件所在的目录(绝对
        log_file_directory = os.path.join(LOG_PATH, t_folder)  # 日志所在的绝对目录

        # 获取日志文件的文件名, 名字中包含时间戳
        log_file_name = py_file_name + time_suffix + ".log"
        log_file_path = os.path.join(log_file_directory, log_file_name)

        # 根据日志文件的绝对路径去创建出所在的目录
        if not os.path.exists(os.path.dirname(log_file_path)):
            os.makedirs(os.path.dirname(log_file_path))
        file = open(log_file_path, 'w')
        file.close()

        # print("最后获得的log_file_path:  ", log_file_path)
        return log_file_path

    def register(self, case_file_path, console=True, default_level=logging.DEBUG, **kwargs):
        # 获取日志文件的绝对路径
        log_file_path = self.get_log_file_name(case_file_path)

        # 封装日志的各种基础配置, 颜色(不同级别的日志的颜色), 格式(时间,文件名,级别,第几行)
        # 设置不同级别的日志在终端中显示的颜色
        log_colors_config = {
            'DEBUG': 'white',  # cyan white
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        # 设置日志文件的格式
        log_format = "%(asctime)s %(filename)s::%(module)s::%(funcName)s[%(lineno)d] %(levelname)s: %(message)s"


        # 给这个日志器挂一个文件句柄和控制台句柄
        logger_name = "main"
        logger = logging.getLogger(logger_name)

        # 给logger挂载一个文件句柄
        file_size_limit = kwargs.get("size_limit", 10*1024*1024)  # 即一个日志文件最大10M
        file_max = kwargs.get("file_max", 6)  # 最多6个文件
        file_mode = kwargs.get("mode", "w")  # 写莫斯
        if log_file_path:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file_path,
                mode=file_mode,
                maxBytes=file_size_limit,
                backupCount=file_max,
                encoding='utf-8'
            )
            file_handler.setFormatter(logging.Formatter(fmt=log_format))
            self.file_handler = file_handler
            logger.addHandler(file_handler)

        # 挂载控制台句柄
        if console:
            stream_handler = logging.StreamHandler()
            console_formatter = colorlog.ColoredFormatter(
                fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
                log_colors=log_colors_config
            )
            stream_handler.setFormatter(console_formatter)
            self.stream_handler = stream_handler
            logger.addHandler(stream_handler)

        # 设置打印日志的基本, 即debu及其以上都打印出来
        logger.setLevel(default_level)

        return logger

    def get_logger(self, logger_name):
        return logging.getLogger(logger_name)

    def unregister(self):
        # 通过getlogger获取日志器
        logger = self.get_logger(logger_name="main")
        # 把日志器的句柄移除, 如果不移除, 就会一直打印日志在之前的文件中
        logger.removeHandler(self.file_handler)
        logger.removeHandler(self.stream_handler)
        pass

def logger_init(case_file_path):
    logger_mgt = LoggerManager()
    logger = logger_mgt.register(case_file_path)
    return logger

def logger_end():
    logger_mgt = LoggerManager()
    logger_mgt.unregister()

