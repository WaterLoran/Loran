import copy

class SingletonMeta(type):
    """
    功能: 实现一个单例模式的基类,只要子类集成这个类即可实现单例模式
    目的: 解决日志管理器在多处调用都能保证是同一个
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


class ServiceContext(metaclass=SingletonMeta):
    def __init__(self):
        # 函数调用计数
        self.func_call_count = {}  # self.func_call_count["add_process"] = 1
        # 最后一个接口自动化用户的账号
        self.last_api_login_user = ""
        # 后置恢复的队列
        self.restore_list = []
        self.restore_switch = True

        # 测试脚本所在目录
        self.test_case_dir = ""

        # 脚本运行时_链条, 用于记录脚本运行到哪一个关键字了, 并做记录, 最后一个节点为未来完结的关键字节点(末节点记录为,script_end)
        self.runtime_chain = []

        # 钩子函数中的信息
        self.base_path = ""
        self.log_path = ""
        self.config_path = ""

        # config目录下的全局config
        self.config = {}

        # 不同环境的authorization授权信息, 即相关的cookie或者token信息
        self.authorization = {}

    def reset_service_context(self):
        self.func_call_count = {}
        self.restore_list = []
        self.runtime_chain = []
        pass

    def _register_func_call(self, func_name=""):
        if func_name in self.func_call_count.keys():
            self.func_call_count[func_name] += 1
        else:
            self.func_call_count[func_name] = 1

    def _get_func_call_count(self, func_name=""):
        return self.func_call_count[func_name]

    def register_func_call_and_get_current_count(self, func_name=""):
        self._register_func_call(func_name=func_name)
        return self._get_func_call_count(func_name=func_name)

    def set_last_api_login_user(self, username):
        self.last_api_login_user = username

    def get_last_api_login_user(self):
        return self.last_api_login_user


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
        self.req_json_script = None
        self.rsp_check = None
        self.auto_fill = None
        self.req_params = None
        self.req_json = None
        self.auto_fill = None
        self.files = None
        self.data = None

        self.rsp_data = None  # 可能为rsp_json, 也可能是rsp.__dict__
        self.default_check_res = None

        self.api_restore = None
        self.cur_restore_flag = False

        self.req_field = None
        self.rsp_field = None

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
        self.req_json_script = None
        self.rsp_check = None
        self.auto_fill = None
        self.req_params = None
        self.req_json = None
        self.auto_fill = None
        self.files = None
        self.data = None

        self.rsp_data = None  # 可能为rsp_json, 也可能是rsp.__dict__
        self.default_check_res = None

        self.api_restore = None
        self.cur_restore_flag = False

        self.req_field = None
        self.rsp_field = None

    def init_step(self, api_type, func, **kwargs):
        self.api_type = api_type  # 请求的类型
        self.func = func  # 测试步骤的说调用的函数名
        self.func_kwargs = copy.deepcopy(kwargs)  # 关键字调用时候的入参
        self.unprocessed_kwargs = kwargs
