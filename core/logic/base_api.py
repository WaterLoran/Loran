import yaml
import requests
import config
from core.init import *



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
        print("env_file_path", env_file_path)
        with open(env_file_path, 'r', encoding='utf-8') as f:
            env_res = yaml.load(f.read(), Loader=yaml.FullLoader)
        print("env_res", env_res)
        return env_res
        env_res = config.config_yaml
        return env_res

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
        rsp = requests.request("post", self.base_url + url, json=login_json)
        rsp_json = rsp.json()
        self.token = rsp_json["token"]

        print("token", self.token)
        pass

    def send(self, method, url="", **kwargs):
        # 需要將token填充到header中， 然後再去請求
        self.get_token()  # 手动执行这个函数, 将token更新到实例变量中
        headers = {}
        headers.update({"Authorization": "Bearer " + self.token})
        if not url.startswith("/"):
            url = "/" + url
            print("请给您的url加上/, 以满足格式要求")
        rsp = requests.request(method, self.base_url + url, headers=headers, **kwargs)
        rsp_data = rsp.json()
        print("url", url)
        print("rsp_data", rsp_data)
        return rsp_data


if __name__ == '__main__':
    api = BaseApi()
    api.get_token()

