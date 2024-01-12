import json
from core.init import *
from .base_api import BaseApi
from .request_data import RequestData
from .response_data import ResponseData
from core.ruoyi_hook.logger import LoggerManager
from ..ruoyi_error import RuoyiError


logger = LoggerManager().get_logger("main")

class Api:
    def __init__(self):
        pass

    def get_api_data(self, api_type, func, **kwargs):
        """
        获取API数据层的数据的方法
        :param api_type: APi的类型
        :param func: API的名称
        :param kwargs:
        :return:
        """
        logger.info(">>>>>>>>>>>>>>>  获取APi层数据 - 开始\n")

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
            raise RuoyiError("get_api_data_failed", func=func.__name__)

        res_list = []
        for item in required_para:
            try:
                res_list.append(api_data[item])
            except Exception as err:  # 期望必须传入的参数, 没有传, 比如url乜有编写
                raise RuoyiError("no_necessary_parameters_were_passed_in", api_type=api_type, func=func, need_para=item)


        # 不要求的参数, 可能会出现
        for item in not_required_para:
            if item in api_data.keys():
                res_list.append(api_data[item])
            else:
                res_list.append(None)
        logger.info("<<<<<<<<<<<<<<<  获取APi层数据 - 结束\n")
        return res_list

    def _get_fetch(**kwargs):
        fetch = None
        if "fetch" in kwargs.keys():
            fetch = kwargs["fetch"]
            del kwargs["fetch"]
            logger.debug(f"_get_fetch::fetch:: {fetch}")
        return fetch, kwargs

    def _get_check(**kwargs):
        check = None
        if "check" in kwargs.keys():
            check = kwargs["check"]
            del kwargs["check"]
            logger.debug(f"业务脚本层传入的主动断言信息::check:: {check}")
        return check, kwargs

    def abstract_api(self, api_type, func, **kwargs):
        """
        抽象API, 即描述各个API的操作前后的所有行为, 包括, APi数据获取, 入参填充, 实际请求, 断言, 提取在响应信息, 日志等
        :param api_type:
        :param func:
        :param kwargs:
        :return:
        """
        logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  测试步骤 - 开始" + func.__name__ + "\n")

        # 将fetch从kwargs中提取出来
        fetch, kwargs = Api._get_fetch(**kwargs)
        # 将check关键字从kwargs中提取出来
        check, kwargs = Api._get_check(**kwargs)
        logger.info(func.__name__ + "::去除fetch和check和的kwargs: " + json.dumps(kwargs))

        # 获取Api数据层的相关数据

        if api_type == "json":
            req_method, req_url, req_json, rsp_check, auto_fill, teardown = Api().get_api_data("json", func, **kwargs)
        elif api_type == "urlencoded":
            req_method, req_url, req_params, req_json, rsp_check, auto_fill, teardown = Api().get_api_data("urlencoded", func, **kwargs)
        elif api_type == "form_data":
            req_method, req_url, files, data, rsp_check = Api().get_api_data("form_data", func, **kwargs)
            pass


        # 将业务脚本层的入参填充到请求体中
        if api_type == "json":
            if auto_fill is not False:  # 为False的时候, 不做填充
                req_json = RequestData().modify_req_body(req_json, **kwargs)
                logger.info(func.__name__ + "  步骤::json类型请求体::" + json.dumps(req_json))
        elif api_type == "urlencoded":
            if auto_fill is not False:  # 为False的时候, 不做填充
                req_params = RequestData().modify_req_body(req_params, **kwargs)
                logger.info(func.__name__ + "  urlencoded类型请求体::" + json.dumps(req_json))
        else:
            pass


        # 做实际请求
        logger.info(f"准备发送请求, url为{req_url}")
        if api_type == "json":  # json类型的请求
            rsp_data = BaseApi().send(method=req_method, url=req_url, json=req_json)
        elif api_type == "urlencoded":  # urlencode类型的请求
            rsp_data = BaseApi().send(method=req_method, url=req_url, params=req_params)
        elif api_type == "form_data":  # form_data类型的请求
            logger.debug(f"form_data类型请求, files参数::files")

            if files is not None:
                # 拼接出绝对路径
                abs_file_path = os.path.join(FILES_PATH, files)
                logger.debug(f"form_data类型请求, 上传文件的绝对路径::{abs_file_path}")
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
        default_check_res = ResponseData().check_api_default_expect(req_data, rsp_data, rsp_check, check)

        # 业务层的主动断言
        logger.info(">>>>>>>>>>>>>>>>  业务层的主动断言-开始\n")
        service_check_res = ResponseData().check_all_expect(rsp_data, check)
        logger.info("<<<<<<<<<<<<<<<<  业务层的主动断言-结束\n")
        # 做提取信息操作
        ResponseData().fetch_all_value(rsp_data, fetch)

        logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  XX步骤-结束" + func.__name__ + "\n")

        if default_check_res and service_check_res:  # 只有业务层的主动断言和APi数据层的默认断言都是成功的, 才会认为这个步骤是执行成功的
            return True
        else:
            return False



    @classmethod
    def json(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            step_check_res = Api().abstract_api("json", func, **kwargs)
            return step_check_res
        return wrapper

    @classmethod
    def urlencoded(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            step_check_res = Api().abstract_api("urlencoded", func, **kwargs)
            print("step_check_res", step_check_res)
            return step_check_res
        return wrapper

    @classmethod
    def form_data(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            step_check_res = Api().abstract_api("form_data", func, **kwargs)
            print("step_check_res", step_check_res)
            return step_check_res
        return wrapper

