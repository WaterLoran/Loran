import jsonpath
import copy
from loran.logger import LoggerManager
from loran.ruoyi_error import RuoyiError
from loran.context import StepContext
from .json_data import JsonData

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


    def fill_context_into_req_json(self, context_input, req_json):
        """
        req_json: 原logic中定义的请求体
        context_input: 业务脚本层中传入的上下文信息
        """
        json_data = JsonData()
        req_json = json_data.merge_a_dict_into_b_dict(context_input, req_json)
        return req_json

    def modify_by_field_define(self, json_dict, **kwargs):
        # 根据传入的field字段名称, 去从 kwargs 去移除
        step_context = StepContext()
        field_define = step_context.req_field

        t_json = copy.deepcopy(json_dict)

        to_rmv_key_list = []

        for key, value in kwargs.items():
            try:
                fill_jsonpath = field_define[key]["jsonpath"] # 这里如果娶不到这个key, 则直接跳过

                # 如果传入的是普通参数, 则直接复制进去, 需要先判断
                # 否则就需要去依赖于生成器去生成数据

                # TODO 这里待编写 generator 函数来生成相关数据
                # generator = field_define[key]["generator"]
                # need_generate = need_to_generate_data(value)
                # if need_generate:
                #     if generator is None:
                #         logger.error("需要使用generator来生成数据, 但是却没有定义")
                #         raise
                #     value= generator_data_entry(generator, value) # 传入业务脚本层的字段的值
                #     print("")

                t_json = JsonData().update_dict_by_jsonpath(
                    data=t_json,
                    jsonpath_expr=fill_jsonpath,
                    new_value=value
                )

                # 使用 field 的信息去填充信息后, 需要将该key从kwargs 中移除, 从而不影响后面的自动填充
                to_rmv_key_list.append(key)
            except:
                # TODO 实际是 使用 lst 查看部门的时候, 抛出异常了, 然后, 就跳到这里了
                logger.debug(f"{key} 入参 在 field 中找不到 jsonpath表达式, 将尝试使用 自动填充方式去填充")

        # 移除那些已经根据 field 去填充进入 json体的key
        for key in to_rmv_key_list:
            del kwargs[key]

        return t_json, kwargs