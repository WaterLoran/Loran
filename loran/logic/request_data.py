import jsonpath
from loran.logger import LoggerManager
from loran.ruoyi_error import RuoyiError


logger = LoggerManager().get_logger("main")



class RequestData:
    def __init__(self):
        self.req_body = None
        self.out_req_data = None
        pass

    def _edit_one_path(self, paths: list, value):
        """
        根据jsonpath路径去请求体中去修改
        :param paths:
        :param value:
        :return:
        """
        alias_of_data = self.req_body
        for path in paths[0:-1]:
            if path.isdigit():  # 是数字的话
                alias_of_data = alias_of_data[int(path)]
            else:               # 不是数字的话
                alias_of_data = alias_of_data[path]

        try:
            if paths[-1].isdigit():
                alias_of_data[int(paths[-1])] = value
            else:
                alias_of_data[paths[-1]] = value
        except Exception:
            raise

        self.req_body = alias_of_data



    def _modify_single(self, key, value):
        """
        使用业务脚本层的单个键值对去对请求体进行修改
        :param key:
        :param value:
        :return:
        """
        # 先找到对应key在请求体中的jsonpath路径
        jsonpath_key = "$.." + key
        found_key_res = jsonpath.jsonpath(self.req_body, jsonpath_key, result_type="IPATH")
        logger.debug(f"found_key_res::{found_key_res}")
        if len(found_key_res) > 1:
            raise RuoyiError("two_or_more_keys_are_found_in_the_request_body", key=key, jsonpath_key=jsonpath_key)

        # 对请求体在中的对应路径的数据进行修改
        paths = found_key_res[0]
        self._edit_one_path(paths, value)


    def modify_req_body(self, req_body, **kwargs):
        """
        对请求体进行入参填充
        :param req_body:
        :param kwargs:
        :return:
        """

        logger.info(">>>>>>>>>>>>>>>  入参填充 - 开始\n")

        # 通过循环对入参键值对进行填充处理
        self.req_body = req_body
        for key, value in kwargs.items():
            logger.debug(f"入参的键值对为 {key}: {value}")
            self._modify_single(key, value)
        logger.info("<<<<<<<<<<<<<<<<  入参填充-结束\n")
        return self.req_body

