import copy
import json
from core.init import *
from config import *
from .base_api import BaseApi
from .request_data import RequestData
from .response_data import ResponseData
from core.ruoyi_hook.logger import LoggerManager
from ..ruoyi_error import RuoyiError

logger = LoggerManager().get_logger("main")


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


class StepContext(metaclass=SingletonMeta):
    """
    用于记录一个测试步骤的上下文信息, 每个关键字第一次调用时置空上下文, 并将自己的原始原始信息存入
    """

    def __init__(self):
        self.api_type = ""  # 请求的类型
        self.func = ""  # 测试步骤的说调用的函数名
        self.func_kwargs = {}  # 关键字调用时候的入参
        self.unprocessed_kwargs = {}  # 请用于存放未处理的入参, 过程中会发生变化

        self.check = None  # 断言信息
        self.fetch = None  # 提取响应信息的表达式

        self.req_method = None
        self.req_url = None
        self.req_json = None
        self.rsp_check = None
        self.auto_fill = None
        self.teardown = None
        self.req_params = None
        self.req_json = None
        self.auto_fill = None
        self.teardown = None
        self.files = None
        self.data = None

        self.rsp_data = None  # 可能为rsp_json, 也可能是rsp.__dict__
        self.default_check_res = None
    def reset_all_context(self):
        self.api_type = ""  # 请求的类型
        self.func = ""  # 测试步骤的说调用的函数名
        self.func_kwargs = {}  # 关键字调用时候的入参
        self.unprocessed_kwargs = {}  # 请用于存放未处理的入参, 过程中会发生变化

        self.check = None  # 断言信息
        self.fetch = None  # 提取响应信息的表达式

        self.req_method = None
        self.req_url = None
        self.req_json = None
        self.rsp_check = None
        self.auto_fill = None
        self.teardown = None
        self.req_params = None
        self.req_json = None
        self.auto_fill = None
        self.teardown = None
        self.files = None
        self.data = None

        self.rsp_data = None  # 可能为rsp_json, 也可能是rsp.__dict__
        self.default_check_res = None

    def init_step(self, api_type, func, **kwargs):
        self.api_type = api_type  # 请求的类型
        self.func = func  # 测试步骤的说调用的函数名
        self.func_kwargs = copy.deepcopy(kwargs)  # 关键字调用时候的入参
        self.unprocessed_kwargs = kwargs


class Api:
    def __init__(self):
        pass

    def get_api_data_by_api_type(self, api_type, func, **kwargs):
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
            "form_data": [["req_method", "req_url"], ["files", "data", "req_params", "rsp_check"]],
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

    def get_fetch(self):
        step_context = StepContext()
        t_kwargs = step_context.unprocessed_kwargs
        fetch = None
        if "fetch" in t_kwargs.keys():
            fetch = t_kwargs["fetch"]
            del t_kwargs["fetch"]
            logger.debug(f"该测试步骤的 fetch表达式为  {fetch}")

        step_context.fetch = fetch

    def get_check(self):
        step_context = StepContext()
        t_kwargs = step_context.unprocessed_kwargs
        check = None
        if "check" in t_kwargs.keys():
            check = t_kwargs["check"]
            del t_kwargs["check"]
            logger.debug(f"业务脚本层的主动断言信息为 check {check}")

        step_context.check = check

    def get_api_data(self):
        step_context = StepContext()
        api_type = step_context.api_type
        func = step_context.func
        kwargs = step_context.unprocessed_kwargs

        if api_type == "json":
            req_method, req_url, req_json, rsp_check, auto_fill, teardown = Api().get_api_data_by_api_type("json", func, **kwargs)
            step_context.req_method = req_method
            step_context.req_url = req_url
            step_context.req_json = req_json
            step_context.rsp_check = rsp_check
            step_context.auto_fill = auto_fill
            step_context.teardown = teardown

        elif api_type == "urlencoded":
            req_method, req_url, req_params, req_json, rsp_check, auto_fill, teardown = \
                Api().get_api_data_by_api_type("urlencoded", func, **kwargs)
            step_context.req_method = req_method
            step_context.req_url = req_url
            step_context.req_params = req_params
            step_context.req_json = req_json
            step_context.rsp_check = rsp_check
            step_context.auto_fill = auto_fill
            step_context.teardown = teardown
        elif api_type == "form_data":
            req_method, req_url, files, data, req_params, rsp_check = \
                Api().get_api_data_by_api_type("form_data", func, **kwargs)
            step_context.req_method = req_method
            step_context.req_url = req_url
            step_context.files = files
            step_context.data = data
            step_context.req_params = req_params
            step_context.rsp_check = rsp_check
        else:
            raise

    def fill_input_para_to_req_body(self):
        step_context = StepContext()
        api_type = step_context.api_type
        auto_fill = step_context.auto_fill
        func = step_context.func
        req_json = step_context.req_json
        req_params = step_context.req_params
        kwargs = step_context.unprocessed_kwargs

        logger.debug(f"做入参填充时接口类型是 {api_type}")
        if api_type == "json":
            if auto_fill is not False:  # 为False的时候, 不做填充
                req_json = RequestData().modify_req_body(req_json, **kwargs)
                step_context.req_json = req_json  # 将信息更新回上下文中
                logger.info(func.__name__ + "  步骤::json类型请求体::" + json.dumps(req_json))
        elif api_type == "urlencoded":
            if auto_fill is not False:  # 为False的时候, 不做填充
                req_params = RequestData().modify_req_body(req_params, **kwargs)
                step_context.req_params = req_params  # 将信息更新回上下文中
                logger.info(func.__name__ + "  urlencoded类型请求体::" + json.dumps(req_params))
        elif api_type == "form_data":
            logger.debug("当前是form_data请求, 不做入参填充, 因为不存在入参填充的场景")
        else:
            logger.debug(f"API的数据类型是{api_type}")
            raise

    def do_real_request(self):
        step_context = StepContext()
        api_type = step_context.api_type
        func = step_context.func
        req_json = step_context.req_json
        req_params = step_context.req_params
        req_url = step_context.req_url
        req_method = step_context.req_method
        files = step_context.files
        data = step_context.data

        logger.info(f"========  开始 {func.__name__} 步骤的请求  ========")
        if api_type == "json":  # json类型的请求
            rsp_data = BaseApi().send(method=req_method, url=req_url, json=req_json)
        elif api_type == "urlencoded":  # urlencode类型的请求
            rsp_data = BaseApi().send(method=req_method, url=req_url, params=req_params, json=req_json)
        elif api_type == "form_data":  # form_data类型的请求
            if files is not None:
                # 拼接出绝对路径
                if isinstance(files, str):
                    logger.error(
                        "这个软件系统上传文件场景, form_data中的那个文件名不统一, 暂时不支持这种使用方法, 即files='XX.png'")
                    raise
                if isinstance(files, dict):
                    for form_key_name, file_name in files.items():
                        abs_file_path = os.path.join(FILES_PATH, file_name)
                        logger.debug(f"form_data类型请求, 上传文件的绝对路径::{abs_file_path}")
                        file_obj = open(abs_file_path, 'rb')
                        files_dict = {form_key_name: file_obj}  # 将文件放入一个字典中，字典的键是'file'
            else:
                files_dict = {}  # 默认没有的时候
            req_body_dict = {
                "method": req_method,
                "url": req_url,
            }
            if files != {}:
                req_body_dict.update({
                    "files": files_dict
                })
            if data is not None:
                req_body_dict.update({
                    "data": data
                })
            if req_params is not None:
                req_body_dict.update({"params": req_params})
            rsp_data = BaseApi().send(**req_body_dict)

            # 此处的rsp_data 可能是rsp_json 或者是 rsp.__init__
        else:
            raise
        logger.info(f"========  结束 {func.__name__} 步骤的请求  ========")
        step_context.rsp_data = rsp_data
        pass

    def do_api_default_check(self):
        step_context = StepContext()
        api_type = step_context.api_type
        func = step_context.func
        req_json = step_context.req_json
        data = step_context.data
        rsp_data = step_context.rsp_data
        rsp_check = step_context.rsp_check
        check = step_context.rsp_check

        logger.info(f"========  开始 {func.__name__} 步骤的 API层默认断言  ========")
        if api_type == "json":  # json类型的请求:
            req_data = req_json
        elif api_type == "form_data":
            req_data = data
        else:  # 其他类型为空, 也就是其他场景下, 目前不会去结合请求体去做断言
            req_data = {}
        default_check_res = ResponseData().check_api_default_expect(req_data, rsp_data, rsp_check, check)
        step_context.default_check_res = default_check_res
        logger.info(f"========  结束 {func.__name__} 步骤的 API层默认断言  ========")
        pass

    def do_service_check(self):
        step_context = StepContext()
        func = step_context.func
        rsp_data = step_context.rsp_data
        check = step_context.check
        fetch = step_context.fetch

        logger.info(f"========  开始 {func.__name__} 步骤的 业务层主动断言  ========")
        print("step_context.__dict__", step_context.__dict__)
        service_check_res = ResponseData().check_all_expect(rsp_data, check)
        logger.info(f"========  结束 {func.__name__} 步骤的 业务层主动断言  ========")

        # 做提取信息操作
        logger.info(f"========  开始 {func.__name__}步骤的 信息提取  ========")
        ResponseData().fetch_all_value(rsp_data, fetch)
        logger.info(f"========  结束 {func.__name__}步骤的 信息提取  ========")

        step_context.service_check_res = service_check_res
        pass

    def get_step_check_res(self):
        step_context = StepContext()
        default_check_res = step_context.default_check_res
        service_check_res = step_context.service_check_res
        if default_check_res and service_check_res:  # 只有业务层的主动断言和APi数据层的默认断言都是成功的, 才会认为这个步骤是执行成功的
            return True
        else:
            return False

    def do_service_fetch(self):
        step_context = StepContext()
        func = step_context.func
        rsp_data = step_context.rsp_data
        fetch = step_context.fetch

        # 做提取信息操作
        logger.info(f"========  开始 {func.__name__}步骤的 信息提取  ========")
        ResponseData().fetch_all_value(rsp_data, fetch)
        logger.info(f"========  结束 {func.__name__}步骤的 信息提取  ========")

        pass

    def abstract_api(self, api_type, func, **kwargs):
        """
        抽象API, 即描述各个API的操作前后的所有行为, 包括, APi数据获取, 入参填充, 实际请求, 断言, 提取在响应信息, 日志等
        :param api_type:
        :param func:
        :param kwargs:
        :return:
        """
        logger.info("\n\n")
        logger.info(f"================  开始 测试步骤 {func.__name__} 测试步骤  ================")

        # 重置测试步骤的所有上下文信息 并初始化
        step_context = StepContext()
        step_context.reset_all_context()
        step_context.init_step(api_type, func, **kwargs)  # 将当前测试步骤的信息初始化到步骤上下文中

        # 将fetch从kwargs中提取出来
        self.get_fetch()

        # 将check关键字从kwargs中提取出来
        self.get_check()

        # 获取Api数据层的相关数据
        self.get_api_data()

        # 将业务脚本层的入参填充到请求体中
        self.fill_input_para_to_req_body()

        # 做实际请求
        self.do_real_request()

        # API数据层的默认断言
        self.do_api_default_check()

        # 业务层的主动断言
        self.do_service_check()
        logger.info(f"================  结束 测试步骤 {func.__name__} 测试步骤  ================")
        return self.get_step_check_res()


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
