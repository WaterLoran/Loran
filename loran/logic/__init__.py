import copy
import json
import time
import allure
import pytest_check
from .base_api import BaseApi
from .request_data import RequestData
from .response_data import ResponseData
from loran.logger import LoggerManager
from loran.ruoyi_error import RuoyiError
from .complex_api import ComplexApi
from easydict import EasyDict as register
from loran.context import *

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
            "json": [["req_method", "req_url", "req_json"], ["rsp_check", "auto_fill", "restore", "req_field", "rsp_field"]],
            "urlencoded": [["req_method", "req_url", "req_params"], ["req_json", "rsp_check", "auto_fill", "restore", "rsp_field"]],
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

    def get_restore(self):
        step_context = StepContext()
        t_kwargs = step_context.unprocessed_kwargs

        restore = False
        if "restore" in t_kwargs.keys():
            restore = t_kwargs["restore"]
            del t_kwargs["restore"]
            logger.debug(f"业务脚本层的 恢复标志位 为 restore {restore}")

        step_context.cur_restore_flag = restore

    def get_req_json(self):
        """
        获取业务接口间上下文信息, 即通常为lst皆苦所查询到的信息
        """
        step_context = StepContext()
        t_kwargs = step_context.unprocessed_kwargs

        req_json_script = None
        if "req_json" in t_kwargs.keys():
            req_json_script = t_kwargs["req_json"]
            del t_kwargs["req_json"]

        step_context.req_json_script = req_json_script

    def do_retry_logic(self):
        service_context = ServiceContext()
        step_context = StepContext()

        remain_retry = service_context.remain_retry
        wrapper_func = service_context.wrapper
        kwargs = step_context.func_kwargs

        if "retry" in kwargs:
            del kwargs["retry"]

        # 循环执行该函数, 并根据结果判断是否继续执行
        retry_count = 0
        while remain_retry > 0:
            remain_retry -= 1
            retry_count += 1
            logger.debug(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 正在尝试第{retry_count}次")

            step_assert_res = wrapper_func(**kwargs)  # 调用函数本身, 但是已经移除retry参数

            if not step_assert_res:  # 成功是结果为成功
                logger.warning(f"第 {retry_count} 次的 尝试执行logic结果为 失败")
            else:  # 重试的结果为成功
                logger.info(f"第 {retry_count} 次的 尝试执行logic结果为 成功")
                # 如果重试成功的话, 则恢复相关的错误堆栈信息 到 这个logic之前, 即从 service_context 中取出这个数据, 并更新
                pytest_check.check_log._num_failures = service_context.stack_pytest_check_num_failures
                pytest_check.check_log._failures = service_context.stack_pytest_check_failures

                # 更新 这个步骤的断言结果, 即这个logic的执行结果,
                # fetch如果有问题, 会直接抛出异常,而不是暂时记录结果, 所以retry功能对fetch不能使用, TODO, 这里考虑如何开发维护框架
                # 实际脚本的写法中, 可通过多次retry去check 成功某个logic之后, 再去fetch, 就能保证可靠性, 就可以规避这个问题
                step_context.step_check_res = True
                step_context.service_check_res = True
                step_context.api_check_res = True
                break  # 跳出这个循环

            time.sleep(1)  # 每次重试之间间隔一秒

        return self.get_step_check_res()


    def get_retry_and_do_retry(self):
        step_context = StepContext()
        service_context = ServiceContext()
        t_kwargs = step_context.unprocessed_kwargs
        func_name = step_context.func.__name__

        has_retry = False
        retry = 0  # 默认是不重新尝试的
        if "retry" in t_kwargs.keys():
            has_retry = True
            logger.debug(f"将要对 {func_name} 函数尝试执行 {retry} 次, 直到成功")
            retry = t_kwargs["retry"]
            if not isinstance(retry, int):
                logger.error("retry参数表示对该logic最多尝试的次数, 仅允许int类型")
                raise
            del t_kwargs["retry"]

            # 如果传入了retry, 才去记录pytest_check 所记录的 断言信息 stack
            service_context.stack_pytest_check_num_failures = copy.deepcopy(
                pytest_check.check_log._num_failures)  # 记录原始的失败次数
            service_context.stack_pytest_check_failures = copy.deepcopy(pytest_check.check_log._failures)  # 记录原始的错误msg

        service_context.remain_retry = retry  # 每次的logic调用, 都会获取并更新这个变量

        # 如果有has_retry, 则执行do_retry_logic
        if has_retry:
            return self.do_retry_logic()

    def get_api_data(self):
        step_context = StepContext()
        api_type = step_context.api_type
        func = step_context.func
        kwargs = step_context.unprocessed_kwargs

        if api_type == "json":
            req_method, req_url, req_json, rsp_check, auto_fill, restore, req_field, rsp_field\
                = Api().get_api_data_by_api_type("json", func, **kwargs)
            step_context.req_method = req_method
            step_context.req_url = req_url
            step_context.req_json = req_json
            step_context.rsp_check = rsp_check
            step_context.auto_fill = auto_fill
            step_context.api_restore = restore  # API中定义的restore, 在这里重命名位api_restore
            step_context.rsp_field = rsp_field
            step_context.req_field = req_field

        elif api_type == "urlencoded":
            req_method, req_url, req_params, req_json, rsp_check, auto_fill, restore, rsp_field = \
                Api().get_api_data_by_api_type("urlencoded", func, **kwargs)
            step_context.req_method = req_method
            step_context.req_url = req_url
            step_context.req_params = req_params
            step_context.req_json = req_json
            step_context.rsp_check = rsp_check
            step_context.auto_fill = auto_fill
            step_context.api_restore = restore  # API中定义的restore, 在这里重命名为api_restore
            step_context.rsp_field = rsp_field
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

    def fill_req_json_script_to_req_body(self):
        """
        将业务脚本层传入的参数填充到请求体中去
        """
        step_context = StepContext()
        api_type = step_context.api_type
        req_json = step_context.req_json
        req_json_script = step_context.req_json_script

        if req_json_script:  # 如果传入的 context_input 不为空, 则对其进行填充
            if api_type == "json":
                req_json = RequestData().fill_context_into_req_json(req_json_script, req_json)
                step_context.req_json = req_json
            elif api_type == "urlencoded":
                # 暂时不处理该场景, 仅处理json类型的请求
                raise
            else:
                raise
                # 暂时不处理该场景, 仅处理json类型的请求
        else:
            # 该logic调用未传入context, 不做处理
            pass

    def push_restore_to_script_context(self):
        """
        推送到 script_context 之前, 需要根据追加 恢复的标记位
        """
        step_context = StepContext()
        cur_restore = step_context.api_restore

        if cur_restore is not None:  # 如果不是 None, 则追加这个 cur_restore_flag 标志位
            cur_restore.update({
                "cur_restore_flag": step_context.cur_restore_flag
            })

        service_context = ServiceContext()
        service_context.restore_list.append(cur_restore)

    def fill_input_para_to_req_body(self):
        step_context = StepContext()
        api_type = step_context.api_type
        auto_fill = step_context.auto_fill
        func = step_context.func
        req_json = step_context.req_json
        req_field = step_context.req_field
        req_params = step_context.req_params
        kwargs = step_context.unprocessed_kwargs

        logger.debug(f"做入参填充时接口类型是 {api_type}")
        if api_type == "json":

            # 先判断有无 field, 只要有都会去根据fill_loca去填充, 因为这个是精确信息, 是高效的
            if req_field is not None:  # 如果 定义了fill_loca, 则先试用fill_loca来填充, 再对剩余参数使用自动填充方式
                # 这里填充后还要将更新后的kwargs回传
                req_json, kwargs = RequestData().modify_by_field_define(req_json, **kwargs)
                step_context.req_json = req_json

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

    def fetch_for_restore(self):
        """
        在step_context.cur_restore_flag为 True的情况下, 根据API定义中的信息去响应中提取信息出来, 等在teardown中去清除数据
        """
        import jsonpath
        step_context = StepContext()
        rsp_data = step_context.rsp_data
        cur_restore_flag = step_context.cur_restore_flag

        service_context = ServiceContext()
        restore = service_context.restore_list.pop()

        if cur_restore_flag is True:  # 这里与前面呼应了, 前面push_store的时候, 也默认将None 加进去
            # 先取出恢复的标记为
            if restore is None:  # 表示API数据层未定义该相关数据 restore
                logger.error(
                    "该关键字在API层未定位restore信息, 即用于恢复的信息, 但是在业务脚本层调用关键字的时候传入restore=True")
                raise
            cur_restore_flag = restore["cur_restore_flag"]
            del restore["cur_restore_flag"]

            # 然后取出恢复函数的相关信息
            func_name, para = restore.popitem()
            # 对所有入参进行遍历
            func_kwargs = {}
            for para_name, rsp_fetch_expression in para.items():
                if isinstance(rsp_fetch_expression, str):
                    json_path_reg = rsp_fetch_expression
                    extra_change = None
                elif isinstance(rsp_fetch_expression, list) and len(rsp_fetch_expression) == 2:
                    json_path_reg = rsp_fetch_expression[0]
                    extra_change = rsp_fetch_expression[1]
                else:
                    logger.error(str(rsp_fetch_expression))
                    raise

                if "$." in json_path_reg:  # 为正则表达式的时候
                    try:
                        fetch_value = jsonpath.jsonpath(rsp_data, json_path_reg)[0]
                    except:
                        logger.error(
                            "使用json_path_reg去响应信息中获取用于restore的信息的时候出错" + str(json_path_reg))
                        raise
                else:  # 不是正则表达式的情况, 即为正常的字符串
                    fetch_value = json_path_reg

                # 对获取到的数据, 做额外的变换操作
                if extra_change is None:
                    pass
                elif extra_change == "to_list":
                    fetch_value = [fetch_value]
                elif extra_change == "to_int":
                    fetch_value = int(fetch_value)
                else:
                    logger.error("目前在获取restore的参数值时, 对参数做额外的操作时, 仅支持改成list和int这两种操作")
                    raise

                func_kwargs.update({para_name: fetch_value})

            restore = {
                func_name: func_kwargs,
                "cur_restore_flag": cur_restore_flag
            }
            service_context.restore_list.append(restore)

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

        logger.info(f"========  开始 {func.__name__} 步骤的 业务层主动断言  ========")
        service_check_res = ResponseData().check_all_expect(rsp_data, check)
        logger.info(f"========  结束 {func.__name__} 步骤的 业务层主动断言  ========")

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
        ResponseData().rsp_fetch_all_value(rsp_data, fetch)
        logger.info(f"========  结束 {func.__name__}步骤的 信息提取  ========")

        pass

    def init_step(self, api_type, func, wrapper, **kwargs):
        # 重置上下文, 并将当前关键字函数的函数名, 请求类型, 请求参数都更新到上下文中去
        step_context = StepContext()
        step_context.reset_all_context()
        step_context.init_step(api_type, func, **kwargs)  # 将当前测试步骤的信息初始化到步骤上下文中

        # 在业务上下文中 更新运行时链条
        service_context = ServiceContext()
        service_context.wrapper = wrapper

    def abstract_api(self, api_type, func, wrapper, **kwargs):
        """
        抽象API, 即描述各个API的操作前后的所有行为, 包括, APi数据获取, 入参填充, 实际请求, 断言, 提取在响应信息, 日志等
        :param api_type:
        :param func:
        :param kwargs:
        :return:
        """
        # 重置测试步骤的所有上下文信息 并初始化
        self.init_step(api_type, func, wrapper, **kwargs)

        # 获取 retry 尝试次数的 标志位, 并做相关处理
        if self.get_retry_and_do_retry():
            return True

        logger.info("\n\n")
        logger.info(f"================  开始 测试步骤 {func.__name__} 测试步骤  ================")

        # 将fetch从kwargs中提取出来
        self.get_fetch()

        # 将check关键字从kwargs中提取出来
        self.get_check()

        # 将restore关键字从kwargs中提取出来
        self.get_restore()

        # 尝试从业务脚本层获取req_json
        self.get_req_json()

        # 获取Api数据层的相关数据
        self.get_api_data()

        # 将业务脚本层的 req_json 与API定义中的 req_json 合并
        self.fill_req_json_script_to_req_body()

        # 将restore信息追加到 service_context中
        self.push_restore_to_script_context()

        # 将业务脚本层的入参填充到请求体中
        self.fill_input_para_to_req_body()

        # 做实际请求
        self.do_real_request()

        # 根据 restore 中的信息去做fetch
        self.fetch_for_restore()

        # API数据层的默认断言
        self.do_api_default_check()

        # 业务层的主动断言
        self.do_service_check()

        # 业务脚本层的信息提取
        self.do_service_fetch()
        logger.info(f"================  结束 测试步骤 {func.__name__} 测试步骤  ================")
        return self.get_step_check_res()


    @classmethod
    def json(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            step_check_res = Api().abstract_api("json", func, wrapper, **kwargs)
            return step_check_res

        return wrapper

    @classmethod
    def urlencoded(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            step_check_res = Api().abstract_api("urlencoded", func, wrapper, **kwargs)
            return step_check_res

        return wrapper

    @classmethod
    def form_data(self, func):
        def wrapper(**kwargs):
            """我是wrapper的注释"""
            step_check_res = Api().abstract_api("form_data", func, wrapper, **kwargs)
            return step_check_res

        return wrapper


service_context = ServiceContext()
config = service_context.config

__all__ = [
    "Api",  # 常用API
    "ComplexApi",  # 复合 APi
    "allure",  # 报告
    "register",  # 注册器
    "config",  # 全局配置
]