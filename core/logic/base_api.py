import json
import yaml
import requests
from easydict import EasyDict
from core.init import *
from core.ruoyi_hook.logger import LoggerManager
from ..ruoyi_error import RuoyiError
from config import *


logger = LoggerManager().get_logger("main")


# 单例模式
class SingletonMeta(type):
    """
    https://refactoringguru.cn/design-patterns/singleton/python/example#example-0
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

class Token(metaclass=SingletonMeta):
    def __init__(self):
        self.token = None

    def read_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

class BaseApi:
    def __init__(self):
        self.base_url = None
        self.username = None
        self.password = None
        self.token = None

        self.env_info_init()

    def env_info_init(self):

        print("config.user.autotest.name", config.user.autotest.name)
        print("config.user.autotest.password", config.user.autotest.password)

        self.base_url = config.env_ip
        self.username = config.env_user
        self.password = config.env_password

    def get_token(self):
        # 首先去指定地方尝试获取token,
        my_token = Token()
        global_token = my_token.read_token()
        if global_token is None:
            logger.debug("全局token实例中暂无token信息, 将去登录获取token")
            # 如果没有的话, 就去做登录请求来更新
            cur_token = self.login()
            my_token.set_token(cur_token)
            self.token = cur_token
        else:
            logger.debug("已从单例模式的token实例中获得token")
            self.token = global_token

    def login(self):
        # 获取验证码的接口
        url = "/dev-api/captchaImage"
        rsp = requests.request("get", self.base_url + url)
        rsp_json = rsp.json()
        uuid = rsp_json["uuid"]

        # login登录的接口
        url = "/dev-api/login"
        login_json = {
            "username": self.username,
            "password": self.password,
            "code": "888",
            "uuid": uuid
        }
        try:
            rsp = requests.request("post", self.base_url + url, json=login_json)
            rsp_json = rsp.json()
            self.token = rsp_json["token"]
        except:
            raise RuoyiError("failed_to_obtain_token", username=self.username, password=self.password)

        logger.debug("token信息::" + self.token)
        return self.token

    def send(self, method, url="", **kwargs):
        logger.info(">>>>>>>>>>>>>>>>  实际请求-开始\n")

        # 需要將token填充到header中， 然後再去請求
        self.get_token()  # 手动执行这个函数, 将token更新到实例变量中
        headers = {}
        headers.update({"Authorization": "Bearer " + self.token})
        if not url.startswith("/"):
            url = "/" + url
            logger.debug("请给您的url加上/, 以满足格式要求")
        rsp = requests.request(method, self.base_url + url, headers=headers, **kwargs)
        rsp_data = rsp.json()
        logger.debug("真实响应体::" + json.dumps(rsp_data))
        logger.info("<<<<<<<<<<<<<<<<  实际请求-结束\n")
        return rsp_data


if __name__ == '__main__':
    api = BaseApi()
    api.get_token()

