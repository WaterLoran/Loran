import pluggy
import requests
from loran.context import ServiceContext
from loran.ruoyi_error import RuoyiError
from loran.logger.logger_interface import logger

hookimpl = pluggy.HookimplMarker("loran")  # 固定写法, 这里表示根据 loran 这个标识符来实例化一个 hookimpl


class LoginPlugin:
    @hookimpl
    def loran_login(self, select="main", user="admin"):
        """
        即登录测试环境的函数
        :param select:
        :param user:
        :return:
        """
        # 通过业务上下文获取配置信息
        service_context = ServiceContext()
        config = service_context.config
        if select == "main":  # 默认环境的登录方法, 这里的读取配置需要提前读取先
            base_url = config.env.main.domain
            username = config.env.main.username
            password = config.env.main.password

            # base_url = "http://127.0.0.1"
            # username = "admin"
            # password = "admin123"

            # 1. 获取验证码的接口
            url = "/dev-api/captchaImage"  # TODO, 需要从配置中读取
            rsp = requests.request("get", base_url + url)
            rsp_json = rsp.json()
            uuid = rsp_json["uuid"]

            # 2. login登录的接口
            url = "/dev-api/login"
            # 如果不是admin用户的话, 则需要从另外一个 配置表 user表中去获取相关数据
            if user != "admin":
                username = config.user[user]["name"]
                password = config.user[user]["password"]
            login_json = {
                "username": username,
                "password": password,
                "code": "888",
                "uuid": uuid
            }
            try:
                rsp = requests.request("post", base_url + url, json=login_json)
                rsp_json = rsp.json()
                token = rsp_json["token"]
            except:
                logger.error(f"登录失败, 账号密码信息为, {username} / {password}")
                raise

            logger.debug("token信息::" + token)

            # 以下是固定用法, service_context.authorization 用来存放 授权信息, main 表示是某个环境的信息, token这个变量可自行定义
            service_context.authorization["main"] = {}
            service_context.authorization["main"]["token"] = token
        else:
            # 被测环境B的登录方法
            token = ""
            print("其他被测环境的登录方法待编写")
            raise
        return token

    @hookimpl
    def loran_update_header(self):
        """
        即使用login步骤获取到的token, 或者cookie等其他鉴权信息, 来填充到headers中
        :return:
        """
        service_context = ServiceContext()
        token = service_context.authorization["main"]["token"]

        headers = {}
        headers.update({"Authorization": "Bearer " + token})
        return headers

    @hookimpl
    def loran_get_authorization(self, select="main"):
        """
        获取鉴权信息的函数, 如果没有获取到的话, 则调用登录接口, 注意, 这里要结合login来编写对应的存储数据的数据结构, 比如 token 这个字段
        :param select:
        :return:
        """
        service_context = ServiceContext()
        if select not in service_context.authorization.keys():
            cur_token = self.loran_login()
        elif "token" not in service_context.authorization[select].keys():  # 如果在这个key里面的话, 就取出来, 否则调用登录
            cur_token = self.loran_login()
        else:
            cur_token = service_context.authorization[select]["token"]
        return cur_token

