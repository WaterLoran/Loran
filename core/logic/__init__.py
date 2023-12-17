from core.init import *
from .base_api import BaseApi
from .request_data import RequeData
from .response_data import ResponseData
from core.logger import LoggerManager

class Api:
    def __init__(self):
        self.logger = LoggerManager().get_logger("main")
        pass

    def get_api_data(self, api_type, func, **kwargs):
        """
        获取API数据层的数据的方法
        :param api_type: APi的类型
        :param func: API的名称
        :param kwargs:
        :return:
        """
        # 描述各类型请求的必须信息和非必须信息
        api_type_field = {
            # Api类型: 必须要有的
            "json": [["req_method", "req_url", "req_json"], ["rsp_check", "auto_fill", "teardown"]],
            "urlencoded": [["req_method", "req_url", "req_params"], ["req_json", "rsp_check", "autofill", "teardown"]],
            "form_data": [["req_method", "req_url"], ["files", "data", "rsp_check"]],
        }
        required_para = api_type_field[api_type][0]
        not_required_para = api_type_field[api_type][1]
        api_data = func(**kwargs)

        if api_data is None:
            print("请确认是否已经编写return locals")  # TODO
            self.logger.warning("请确认是否已经编写return locals")
            raise
            # raise RuoyiError("the_api_data_is_none")

        res_list = []
        for item in required_para:
            try:
                res_list.append(api_data[item])
            except Exception as err:
                raise  # TODO
                # raise RuoyiError("api_data_has_no_such_field", item=item)

        # 不要求的参数, 可能会出现
        for item in not_required_para:
            if item in api_data.keys():
                res_list.append(api_data[item])
            else:
                print(f" {item} 参数不在Api_data中")
                res_list.append(None)
        return res_list

    def _get_fetch(**kwargs):
        fetch = None
        if "fetch" in kwargs.keys():
            fetch = kwargs["fetch"]
            del kwargs["fetch"]
            print("fetch", fetch)
        return fetch, kwargs

    def _get_check(**kwargs):
        check = None
        if "check" in kwargs.keys():
            check = kwargs["check"]
            del kwargs["check"]
            print("check", check)
        return check, kwargs

    def abstract_api(self, api_type, func, **kwargs):
        """
        抽象API, 即描述各个API的操作前后的所有行为, 包括, APi数据获取, 入参填充, 实际请求, 断言, 提取在响应信息, 日志等
        :param api_type:
        :param func:
        :param kwargs:
        :return:
        """
        # 将fetch从kwargs中提取出来
        fetch, kwargs = Api._get_fetch(**kwargs)

        # 将check关键字从kwargs中提取出来
        check, kwargs = Api._get_check(**kwargs)

        # 获取Api数据层的相关数据
        if api_type == "json":
            req_method, req_url, req_json, rsp_check, auto_fill, teardown = Api().get_api_data("json", func, **kwargs)
        elif api_type == "urlencoded":
            req_method, req_url, req_params, req_json, rsp_check, auto_fill, teardown = Api().get_api_data("urlencoded", func, **kwargs)
        elif api_type == "form_data":
            req_method, req_url, files, data, rsp_check = Api().get_api_data("form_data", func, **kwargs)
            pass

        self.logger.info(f"开始处理新的请求, url为{req_url}")

        print("开始做入参填充")
        # 将业务脚本层的入参填充到请求体中
        if api_type == "json":
            if auto_fill is not False:  # 为False的时候, 不做填充
                req_json = RequeData().modify_req_body(req_json, **kwargs)
                print("req_json", req_json)
        elif api_type == "urlencoded":
            if auto_fill is not False:  # 为False的时候, 不做填充
                req_params = RequeData().modify_req_body(req_params, **kwargs)
                print("req_params", req_params)
        else:
            pass
        print("结束入参填充")


        # 做实际请求
        if api_type == "json":  # json类型的请求
            rsp_data = BaseApi().send(method=req_method, url=req_url, json=req_json)
        elif api_type == "urlencoded":  # urlencode类型的请求
            rsp_data = BaseApi().send(method=req_method, url=req_url, params=req_params)
        elif api_type == "form_data":  # form_data类型的请求
            print(">>files", files)
            print("FILES_PATH", FILES_PATH)

            if files is not None:
                # 拼接出绝对路径
                abs_file_path = os.path.join(FILES_PATH, files)
                print("abs_file_path", abs_file_path)
                file_obj = open(abs_file_path, 'rb')
                files_dict = {'avatarfile': file_obj}  # 将文件放入一个字典中，字典的键是'file'
            else:
                files_dict = {}   # 默认没有的时候
            rsp_data = BaseApi().send(method=req_method, url=req_url, files=files_dict, data=data)

        # API数据层的默认断言
        if api_type == "json":  # json类型的请求:
            req_data = req_json
        elif api_type == "form_data":
            req_data = data
        else:  # 其他类型为空, 也就是其他场景下, 目前不会去结合请求体去做断言
            req_data = {}
        ResponseData().check_api_default_expect(req_data, rsp_data, rsp_check, check)


        # 业务层的主动断言
        ResponseData().check_all_expect(rsp_data, check)

        # 做提取信息操作
        ResponseData().fetch_all_value(rsp_data, fetch)


    @classmethod
    def json(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            Api().abstract_api("json", func, **kwargs)

        return wrapper

    @classmethod
    def urlencoded(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            Api().abstract_api("urlencoded", func, **kwargs)

        return wrapper

    @classmethod
    def form_data(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            Api().abstract_api("form_data", func, **kwargs)

        return wrapper

