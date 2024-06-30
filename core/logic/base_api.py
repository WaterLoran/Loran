import json
import requests
from core.logger import LoggerManager
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

        self.base_url = config.env.main.domain
        self.username = config.env.main.username
        self.password = config.env.main.password

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

    def login(self, user="admin"):
        # 获取验证码的接口
        url = "/dev-api/captchaImage"
        rsp = requests.request("get", self.base_url + url)
        rsp_json = rsp.json()
        uuid = rsp_json["uuid"]

        # login登录的接口
        url = "/dev-api/login"
        if user != "admin":
            self.username = config.user[user]["name"]
            self.password = config.user[user]["password"]
            print("login::self.username", self.username)
            print("login::self.password", self.password)
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

    def update_token(self, user=""):
        if user == "":
            raise
        my_token = Token()
        cur_token = self.login(user=user)
        my_token.set_token(cur_token)
        pass

    def send(self, method, url="", **kwargs):
        logger.info(">>>>>>>>>>>>>>>>  实际请求-开始\n")

        # 需要將token填充到header中， 然後再去請求
        self.get_token()  # 手动执行这个函数, 将token更新到实例变量中
        headers = {}
        headers.update({"Authorization": "Bearer " + self.token})
        if not url.startswith("/"):
            url = "/" + url
            logger.debug("请给您的url加上/, 以满足格式要求")

        self.log_req_info_before_request(url=url, method=method, **kwargs)
        rsp = requests.request(method, self.base_url + url, headers=headers, **kwargs)
        try:
            rsp_data = rsp.json()
            logger.info("真实响应体::" + json.dumps(rsp_data, indent=2, ensure_ascii=False))
        except:
            rsp_data = rsp.__dict__
            logger.info(f"{url}接口的响应(非常规响应而是可能会带有二进制文件的)::rsp_dict: \n  " + str(rsp_res))
        logger.info("<<<<<<<<<<<<<<<<  实际请求-结束\n")
        return rsp_data

    def log_req_info_before_request(self, **kwargs):
        req_url = kwargs["url"]

        req_json_list = ["json", "form_data", "params", "data", "req_json"]
        for body in req_json_list:
            if body in kwargs.keys():
                body_value = kwargs[body]
                if isinstance(body_value, dict):
                    logger.info(f"{req_url}接口的请求体{body}为:: " + json.dumps(body_value, indent=2, ensure_ascii=False))
                else:
                    logger.info(f"{req_url}接口的请求体{body}为:: \n  " + str(body_value))
                    # TODO 需要针对列表类型, 使用pprint来打印
        logger.debug("")


if __name__ == '__main__':
    api = BaseApi()
    api.get_token()

