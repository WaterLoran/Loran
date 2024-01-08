import json
import functools
import jsonpath
from core.page.ui_init import *
from core.ruoyi_hook.logger import LoggerManager
from ..ruoyi_error import RuoyiError

logger = LoggerManager().get_logger("main")


class Page:
    def judge_action_data_type(self, page_node_input):

        logger.debug("judge_action_data_type函数输入的page_node_input变量为" + str(page_node_input))
        element_key = page_node_input[0]  # 入参的名称
        element_value = page_node_input[1]  # 入参的值
        if isinstance(element_value, str):
            action_data_type = "string"
        elif isinstance(element_value, dict):
            action_data_type = "dict"
        else:
            raise
        logger.debug("入参的类型是" + action_data_type)
        return action_data_type

    def extract_action_info(self, page_node_input, page_data):
        action_info = {}  # 最终提取出来的操作信息
        action_data_type = Page().judge_action_data_type(page_node_input)
        if action_data_type == "string":
            # 判断page_node_input的值是 click(关键字) 还是其他字符串(这种场景其实就是要往输入框中输入信息)
            input_key = page_node_input[0]
            input_value = page_node_input[1]
            logger.debug(f"操作的页面节点为 {input_key} , 操作行为或者输入的值为 {input_value}")

            #  去page数据中找到这个节点的相关数据
            jsonpath_regex = f"$..{input_key}"
            try:
                tartget_obj = jsonpath.jsonpath(page_data, jsonpath_regex)[0] # TODO 这里补鞥呢正常执行, 即到page中找不到相关数据, 需要抛出异常 raise
            except:
                # raise RuoyiError("ui_can_not_find_node_in_page_properties", input_key=input_key)
                raise

            location = tartget_obj["location"]  #TODO 需要针对这里的场景做一个前作的location_info的提取, 并且追加到loaction_info中
            by = location[0]
            loca_expression = location[1]
            logger.debug("在page_data中提取到的的node信息为 \n" + json.dumps(tartget_obj, indent=2, ensure_ascii=False))

            # 针对传入的键值对的值, 的信息, 来解析出说要操作的信息
            if input_value.upper() == "CLICK":
                action = "click"
                action_info.update({
                    "by": by,
                    "loca_expression": loca_expression,
                    "action": action
                })
            else:  # 这种场景下, 就是要去给输入框输入一些文字信息了
                # TODO
                pass

        return action_info

    def action(self, **kwargs):
        """
        CLICK: 点击
        INPUT: 输入
        MOVE_HERE: 移动到这里 HOVER(悬浮)
        """
        from seleniumbase import BaseCase
        sb = get_sb_instance()
        sb: BaseCase

        # 从action_info中去提取出操作和定位的相关信息
        by = kwargs["by"]
        loca_expression = kwargs["loca_expression"]
        action = kwargs["action"]

        if action.upper() == "CLICK":
            logger.info(f"将以{by}方式以 {loca_expression} 值去查找元素, 然后点击")
            sb.click(loca_expression, by=by)

        elif action.upper() == "INPUT" or action.upper() == "TYPE":
            if "input_content" not in kwargs.keys():
                print("kwargs", kwargs)
                raise  # TODO 这里要封装没有对应key的异常
            input_content = kwargs["input_content"]

            if by.upper() == "ID":  # seleniumbase中不支持ID方式定位, 这里将他转换为CSS的方式
                loca_expression = "#" + loca_expression
                by = "css selector"

            logger.info(f"将以{by}方式以 {loca_expression} 值去元素去定位, 然后输入字符串 {input_content} ")
            sb.type(loca_expression, input_content, by=by)

        elif action.upper() in ["MOVE_HERE", "HOVER"]:
            logger.info(f"将以{by}方式以 {loca_expression} 值去元素查找, 然后移动鼠标到这个位置")

            sb.hover(by, loca_expression)

    def do_all_web_operation(self, page_data, operation_list):
        for page_node_input in operation_list:
            action_info = Page().extract_action_info(page_node_input, page_data)
            Page().action(**action_info)
        pass

    def get_operation_list(self, **kwargs):
        """
        从业务脚本层的page调用中去获取key-value键值对信息, 即节点和对应操作的信息
        :param kwargs:
        :return:
        """
        operation_list = []
        to_del_key_list = []
        for key, value in kwargs.items():
            operation_list.append([key, value])
            to_del_key_list.append(key)  # 每个提取出来的都要删除
        for key in to_del_key_list:
            del kwargs[key]

        return operation_list, kwargs

    def get_page_data(self, func, **kwargs):
        page_func = func(**kwargs)
        try:
            page_data = page_func["page"]
        except:
            # raise RuoyiError("ui_can_not_get_page")
            raise  # TODO 需要封装对应的异常信息
        logger.info("当前处理的PAGE页面名称是 ==> " + func.__name__)
        logger.debug(json.dumps(page_data, indent=2, ensure_ascii=False))
        return page_data


    @classmethod
    def base(self, func):
        @functools.wraps(func)
        def wrapper(**kwargs):
            """我是 wrapper 的注释"""

            # 做入参信息的提取
            operation_list, kwargs = Page().get_operation_list(**kwargs)

            ## 从记录page数据的函数中获取所有的数据, 并解析出来
            page_data = Page().get_page_data(func)

            # 对入参进行遍历, 依次从page数据中取出对应元素, 识别, 并做对应的操作
            Page().do_all_web_operation(page_data, operation_list)


        return wrapper