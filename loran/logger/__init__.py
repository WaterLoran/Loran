import os
import time
import logging
import logging.handlers
import colorlog
from loran.context import ServiceContext
import threading

class SingletonMeta(type):
    """
    功能: 实现一个单例模式的基类,只要子类集成这个类即可实现单例模式
    目的: 解决日志管理器在多处调用都能保证是同一个
    https://refactoringguru.cn/design-patterns/singleton/python/example#example-0
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class LoggerManager(metaclass=SingletonMeta):
    def __init__(self):
        self.file_handler = None
        self.stream_handler = None
        pass

    # 更简洁的路径回溯实现
    def get_log_file_name(self, case_file_path):
        # 获取cases目录后的相对路径
        cases_index = case_file_path.find("cases")
        if cases_index == -1:
            raise ValueError("测试用例路径中未找到'cases'目录")

        relative_path = case_file_path[cases_index + len("cases") + 1:]
        base_name = os.path.splitext(os.path.basename(relative_path))[0]

        # 生成日志路径
        service_context = ServiceContext()
        log_dir = os.path.join(service_context.log_path, os.path.dirname(relative_path), base_name) # 如果每个脚本的日志都要有一个独立的目录, 则加上base_name
        os.makedirs(log_dir, exist_ok=True)

        # 添加时间戳
        timestamp = time.strftime("_%Y%m%d_%H%M%S")
        return os.path.join(log_dir, f"{base_name}{timestamp}.log")

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

def get_logger():
    logger_mgt = LoggerManager()
    logger = logger_mgt.get_logger("main")
    return logger

