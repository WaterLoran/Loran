import json
import functools
import jsonpath
import pytest_check
from core.page.ui_init import *
from core.logger import LoggerManager
from core.ruoyi_error import RuoyiError

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
        elif isinstance(element_value, list):
            action_data_type = "list"
        else:
            raise
        logger.debug("入参的类型是" + action_data_type)
        return action_data_type

    def extract_one_check_info(self, page_data, page_node_input):
        action_info = {}
        #             last_user_name=["text", "eq", "loran888"]
        input_key = page_node_input[0]  # input_key 就是 user_node_delete_button
        jsonpath_regex = f"$..{input_key}"  # 获取目标信息的jsonpath表达式
        print("jsonpath_regex", jsonpath_regex)
        try:
            tartget_obj = jsonpath.jsonpath(page_data, jsonpath_regex)[0]  # 找出在page中的目标数据
        except:
            # raise RuoyiError("ui_can_not_find_node_in_page_properties", input_key=input_key)
            raise  # TODO 封装异常

        location = tartget_obj["location"]  # 找出定位方法
        by = location[0]
        loca_expression = location[1]

        input_list = page_node_input[1]
        # input_list 就是 ["text", "eq", "loran888"],  如果是断言可见性的话["visible", True],

        action = "CHECK"
        attribute = input_list[0]
        if attribute.upper() == "TEXT":
            compare_type = input_list[1]
            target = input_list[2]
            action_info.update({  # 更新定位方法, 定位信息, 和操作行为
                "by": by,
                "loca_expression": loca_expression,
                "action": action,
                "attribute": attribute,
                "compare_type": compare_type,
                "target": target  # 期望的结果
            })
        elif attribute.upper() == "VISIBLE":
            state = input_list[1]
            action_info.update({  # 更新定位方法, 定位信息, 和操作行为
                "by": by,
                "loca_expression": loca_expression,
                "action": action,
                "attribute": attribute,
                "state": state,
            })
        elif attribute.upper() in ["CLICKABLE", "ENABLED"]:
            state = input_list[1]
            action_info.update({  # 更新定位方法, 定位信息, 和操作行为
                "by": by,
                "loca_expression": loca_expression,
                "action": action,
                "attribute": attribute,
                "state": state,
            })
        return action_info

    def organize_into_two_dimensional_check(self, page_node_input):
        # page_node_input[0] = last_user_user_name
        # page_node_input[1] = [["text", "eq", var_user_name],["visible", True]],
        # 最后的输出应该为   [
        #     ["last_user_user_name", ["text", "eq", "var_user_name"]]
        #     ["last_user_user_name", ["visible", True]]
        # ]
        check_info_type = "two"
        for item in page_node_input[1]:
            if not isinstance(item, list):  #只要某一个元素的类型不是列表, 那么传入的就是一维列表
                check_info_type = "one"

        if check_info_type == "one":  # 只有一个断言信息的时候
            page_node_input_list = [page_node_input]

        elif check_info_type == "two":  # 有两个断言信息的时候
            page_node_input_list = []
            for one_check in page_node_input[1]:
                t_page_node_input = [page_node_input[0], one_check]
                page_node_input_list.append(t_page_node_input)
            print("page_node_input_list", page_node_input_list)
        return page_node_input_list

    def extract_one_operation_info(self, page_data, page_node_input):
        action_info = {}
        action_info_list = []
        input_key = page_node_input[0]
        input_value = page_node_input[1]
        logger.debug(f"操作的页面节点为 {input_key} , 操作行为或者输入的值为 {input_value}")

        #  去page数据中找到这个节点的相关数据
        jsonpath_regex = f"$..{input_key}"
        try:
            tartget_obj = jsonpath.jsonpath(page_data, jsonpath_regex)[
                0]  # TODO 这里补鞥呢正常执行, 即到page中找不到相关数据, 需要抛出异常 raise
        except:
            # raise RuoyiError("ui_can_not_find_node_in_page_properties", input_key=input_key)
            raise

        location = tartget_obj["location"]  # TODO 需要针对这里的场景做一个前作的location_info的提取, 并且追加到loaction_info中
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
        else:  # 在输入的value 为字符串的情况下, 不是点击(click)的话, 那就只能说明这个字符串是要输入的信息了, 并且对应的组件的默认操作一定是输入
            default_action = tartget_obj["default_action"]  # 有且仅仅能够为type
            action = default_action
            input_content = input_value
            action_info.update({
                "by": by,
                "loca_expression": loca_expression,
                "action": action,
                "input_content": input_content
            })
        action_info_list.append(action_info)
        return action_info_list
    def extract_one_operation_info_with_para(self, page_data, page_node_input):
        action_info = {}
        action_info_list = []
        #             user_node_delete_button={
        #                 "var_user_name": var_user_name,
        #                 "action": "click"
        #             }
        input_key = page_node_input[0]  # input_key 就是 user_node_delete_button
        jsonpath_regex = f"$..{input_key}"  # 获取目标信息的jsonpath表达式
        try:
            tartget_obj = jsonpath.jsonpath(page_data, jsonpath_regex)[0]  # 找出在page中的目标数据
        except:
            # raise RuoyiError("ui_can_not_find_node_in_page_properties", input_key=input_key)
            raise  # TODO 封装异常

        location = tartget_obj["location"]  # 找出定位方法
        by = location[0]
        loca_expression = location[1]

        input_dict = page_node_input[1]
        # input_dict 就是 {
        #                 "var_user_name": var_user_name,
        #                 "action": "click"
        #           }
        if "action" not in input_dict.keys():
            raise

        action = input_dict["action"]

        for key, value in input_dict.items():  # 对那些出关键字之外的信息, 做相关填充, 和替换
            if key not in ["action", "check", "fetch"]:  # 这里的设计是将那些 除 关键字之外的信息, 都填充到location中去
                loca_expression = loca_expression.replace(key, value)

        action_info.update({  # 更新定位方法, 定位信息, 和操作行为
            "by": by,
            "loca_expression": loca_expression,
            "action": action
        })
        action_info_list.append(action_info)
        return action_info_list

    def extract_action_info(self, page_node_input, page_data):
        action_info = {}  # 最终提取出来的操作信息
        action_info_list = []
        action_data_type = Page().judge_action_data_type(page_node_input)
        if action_data_type == "string":
            # 判断page_node_input的值是 click(关键字) 还是其他字符串(这种场景其实就是要往输入框中输入信息)
            action_info_list = Page().extract_one_operation_info(page_data, page_node_input)
            print("action_info_list", action_info_list)

        elif action_data_type == "dict":
            action_info_list = Page().extract_one_operation_info_with_para(page_data, page_node_input)

        elif action_data_type == "list":  # 表示要做多个断言
            # 先判断是二维列表, 还是一维列表, 然后统一层二维列表
            # 然后依次对二维列表中的, 断言信息进行信息提取
            # 最终返回, 字典列表, 也就是一个列表里面, 有多个字典, 每个字典就是一个操作信息
            check_list = Page().organize_into_two_dimensional_check(page_node_input)
            for page_node_input in check_list:
                action_info = Page().extract_one_check_info(page_data, page_node_input)
                action_info_list.append(action_info)

        logger.debug(f"根据{str(page_node_input)}提取到的操作信息为" + json.dumps(action_info, indent=2, ensure_ascii=False))
        return action_info_list

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

        elif action.upper() in ["CHECK"]:
            logger.info(f"将以{by}方式以 {loca_expression} 值去元素查找, 然后找到文本, 再去做一个文本断言")

            attribute = kwargs["attribute"]  # 获取断言的, 关键属性, 可选的有  TEXT  VISIBLE

            if attribute.upper() == "TEXT":
                compare_type = kwargs["compare_type"]
                target = kwargs["target"]
                compare_type = Page().get_unify_compare_symbol(compare_type)
                if compare_type == "equal":
                    sb.assert_text_visible(target, loca_expression, by=by)
                elif compare_type == "not_equal":
                    sb.assert_text_not_visible(target, loca_expression, by=by)
            elif attribute.upper() == "VISIBLE":
                state = kwargs["state"]
                if state is True:  # 为True的情况
                    sb.assert_element_visible(loca_expression, by=by)
                elif state is False:
                    sb.assert_element_not_visible(loca_expression, by=by)  # 表示断言不可见
                else:
                    raise
            elif attribute.upper() in ["CLICKABLE", "ENABLED"]:
                state = kwargs["state"]
                clickable_state = sb.is_element_clickable(loca_expression, by=by)
                print("clickable_state", clickable_state)
                print("state", state)
                if state is True:  # 为True的情况
                    pytest_check.assert_equal(clickable_state, True)
                elif state is False:
                    pytest_check.assert_equal(clickable_state, False)
                else:
                    raise
            elif attribute.upper() == "PRESENT":
                state = kwargs["state"]
                if state is True:  # 为True的情况
                    sb.assert_element_present(loca_expression, by=by)
                elif state is False:
                    sb.assert_element_not_present(loca_expression, by=by)  # 表示断言不可见
                else:
                    raise


    def get_unify_compare_symbol(self, symbol):
        compare_dict = {
            "equal": ["==", "eq", "equal"],
            "not_equal": ["!=", "not_equal", "not_eq"],
            # "greater": [">", "lg", "larger", "greater"],
            # "less": ["<", "smaller", "less"],
            # "greater_equal": [">=", "greater_equal"],
            # "less_equal": ["<=", "less_equal"],
            # "in": ["in"],
            # "not_in": ["not_in"],
            # "include": ["include"],
            # "not_include": ["not_include"],
        }
        for key, value in compare_dict.items():
            if symbol in value:
                return key
        raise RuoyiError("the_comparator_is_not_defined", symbol=symbol, compare_dict=compare_dict)

    def compare_action(self, compared_obj, compare_type, target):
        if compare_type == "equal":
            pytest_check_result = pytest_check.equal(compared_obj, target)
        elif compare_type == "not_equal":
            pytest_check_result = pytest_check.not_equal(compared_obj, target)
        elif compare_type == "greater":
            pytest_check_result = pytest_check.greater(compared_obj, target)
        elif compare_type == "greater_equal":
            pytest_check_result = pytest_check.greater_equal(compared_obj, target)
        elif compare_type == "less":
            pytest_check_result = pytest_check.less(compared_obj, target)
        elif compare_type == "less_equal":
            pytest_check_result = pytest_check.less_equal(compared_obj, target)
        elif compare_type == "in":
            pytest_check_result = pytest_check.is_in(compared_obj, target)
        elif compare_type == "not_in":
            pytest_check_result = pytest_check.is_not_in(compared_obj, target)
        elif compare_type == "include":
            pytest_check_result = pytest_check.is_in(target, compared_obj)
        elif compare_type == "not_include":
            pytest_check_result = pytest_check.is_not_in(target, compared_obj)
        else:
            raise

        return pytest_check_result


    def do_all_web_operation(self, page_data, operation_list):
        for page_node_input in operation_list:
            action_info_list = Page().extract_action_info(page_node_input, page_data)
            for action_info in action_info_list:
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