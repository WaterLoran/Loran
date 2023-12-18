from core.logger import LoggerManager


logger = LoggerManager().get_logger("main")

class RuoyiError(Exception):
    def __init__(self, error_key, **kwargs):
        error_dict = {
            "get_api_data_failed": "从API数据层获取数据失败, 排查思路: 1. 请确认API数据层的关键字函数中是否有编写return locals()",
            "no_necessary_parameters_were_passed_in": "没有传入必要的参数, 排查思路: 1. 请根据各类型请求检查必须的参数, 请到框架中搜索api_type_field并执行排查",
            "two_or_more_keys_are_found_in_the_request_body": "在请求体中找到了2个或以上的相同的key, 即不能满足自动填充入参的场景, 排查思路: 1. 请求体是否编写错误 2. 该APi关键字不要采用自动入参填充方式, 可以在请求体中直接引用形参, 并写auto_fill = False",
            "the_comparator_is_not_defined": "该比较符未被定义 排查思路: 1. 编写的比较符号和实际定义的有文字上的出入 2.说想要的比较方式还未定义, 请联系框架作者编写对应比较符及其功能",
            "failed_to_obtain_token": "获取token失败 排查思路: 1. 账号密码错误 2.在测试环境中该账号已经被注销"
        }
        self.error_info = error_dict[error_key]
        for key, value in kwargs.items():
            key_info = "\n  辅助信息 ==> key: {}, value: {}".format(key, value)
            self.error_info += key_info

        logger.error(str(self.error_info))

    def __str__(self):
        return repr(self.error_info)
