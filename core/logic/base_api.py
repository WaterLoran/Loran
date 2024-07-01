import json
import requests
from core.logger import LoggerManager
from core.context import ServiceContext
from core.ruoyi_error import RuoyiError
from core.logic.login_plugin import *

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


class BaseApi:
    def __init__(self):
        self.base_url = None
        self.username = None
        self.password = None
        self.env_info_init()

    def env_info_init(self):

        config = ServiceContext().config
        self.base_url = config.env.main.domain
        self.username = config.env.main.username
        self.password = config.env.main.password

    def get_authorization(self, select="main"):
        # TODO, 要区分环境 select
        # 尝试去获取相关的token信息
        cur_authorization = get_authorization_interface()
        return cur_authorization  # 返回用于调试

    def login(self, user="admin"):
        cur_token = login_plugin_interface()  # TODO, 需要处理不同的用户
        return cur_token

    def update_header(self):
        headers = update_headers_interface()
        return headers

    def send(self, method, url="", **kwargs):
        logger.info(">>>>>>>>>>>>>>>>  实际请求-开始\n")

        # 需要將token填充到header中， 然後再去請求

        self.get_authorization()  # 手动执行这个函数, 将token更新到实例变量中

        headers = self.update_header()  # 将来 还要支持在关键字中去修改 的那个logic的headers

        # TODO, 需要根据业务脚本层传入到额 headers 去更新当前的headers

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
            logger.info(f"{url}接口的响应(非常规响应而是可能会带有二进制文件的)::rsp_dict: \n  " + str(rsp))
        logger.info("<<<<<<<<<<<<<<<<  实际请求-结束\n")
        return rsp_data

    def log_req_info_before_request(self, **kwargs):
        req_url = kwargs["url"]

        req_json_list = ["json", "form_data", "params", "data", "req_json"]
        for body in req_json_list:
            if body in kwargs.keys():
                body_value = kwargs[body]
                if isinstance(body_value, dict):
                    logger.info(
                        f"{req_url}接口的请求体{body}为:: " + json.dumps(body_value, indent=2, ensure_ascii=False))
                else:
                    logger.info(f"{req_url}接口的请求体{body}为:: \n  " + str(body_value))
                    # TODO 需要针对列表类型, 使用pprint来打印
        logger.debug("")


if __name__ == '__main__':
    # >>>>>>>> 加载配置,此段代码不修改, 用于手工加载配置, 用于调试, 可能需要修改 config_path 成当前调试的路径
    from core.utils.read_all_yaml_to_config import load_all_config_base_config_path

    config = load_all_config_base_config_path(config_path="E:\Develop\RuoYiTest\config")
    service_context = ServiceContext()
    service_context.config = config
    # <<<<<<<< 加载配置,此段代码不修改, 用于手工加载配置, 用于调试, 可能需要修改 config_path 成当前调试的路径

    api = BaseApi()

    authorization_info = api.get_authorization()
    print("authorization_info", authorization_info)

    headers = api.update_header()
    print("headers    ", headers)
