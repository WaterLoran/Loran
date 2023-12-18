import json
import yaml
import requests
import config
from core.init import *
from core.logger import LoggerManager
from ..ruoyi_error import RuoyiError

logger = LoggerManager().get_logger("main")



class BaseApi:
    def __init__(self):
        self.base_url = None
        self.username = None
        self.password = None
        self.token = None

        self.env_info_init()
        pass

    def env_info_init(self):
        env_res = self.read_env_yaml()
        self.base_url = env_res["env_ip"]
        self.username = env_res["env_user"]
        self.password = env_res["env_password"]
        pass

    def read_env_yaml(self):
        env_file_path = os.path.join(CONFIG_PATH, "environment.yaml")
        with open(env_file_path, 'r', encoding='utf-8') as f:
            env_res = yaml.load(f.read(), Loader=yaml.FullLoader)
        return env_res
        # env_res = config.config_yaml
        # return env_res

    def get_token(self):
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
        rsp = requests.request(method, self.base_url + url, headers=headers, **kwargs)
        rsp_data = rsp.json()
        logger.debug("真实响应体::" + json.dumps(rsp_data))
        logger.info("<<<<<<<<<<<<<<<<  实际请求-结束\n")
        return rsp_data


if __name__ == '__main__':
    api = BaseApi()
    api.get_token()

