import pytest_check
from loran.ruoyi_error import RuoyiError
from loran.logger.logger_interface import logger
import json
import jsonpath
from loran.context import *

def compare_action(compared_obj, compare_type, target):
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


def get_unify_compare_symbol(symbol):
    compare_dict = {
        "equal": ["==", "eq", "equal"],
        "not_equal": ["!=", "not_equal", "not_eq"],
        "greater": [">", "lg", "larger", "greater"],
        "less": ["<", "smaller", "less"],
        "greater_equal": [">=", "greater_equal"],
        "less_equal": ["<=", "less_equal"],
        "in": ["in"],
        "not_in": ["not_in"],
        "include": ["include"],
        "not_include": ["not_include"],
    }
    for key, value in compare_dict.items():
        if symbol in value:
            return key
    raise RuoyiError("the_comparator_is_not_defined", symbol=symbol, compare_dict=compare_dict)


def check_obj(obj=None, attr="value", assert_type="", target=""):
    if attr not in ["value", "length", "type"]:
        logger.error("使用check_obj函数时, attr暂仅允许 value, length, type这些枚举值, 即对象的属性")
        raise

    if attr == "value":
        raise
    elif attr == "length":
        compared_obj = len(obj)
        assert_type = get_unify_compare_symbol(assert_type)
        compare_action(compared_obj, assert_type, target)
    elif attr == "type":
        raise


def check_json_with_one_expect(rsp_data, each_check):
    jsonpath_regex = each_check[0]
    compare_symbol = each_check[1]
    target = each_check[2]

    if compare_symbol == "exist":  # 如果是为了某个jsonpath表达式在响应中是否存在
        fetch_res = jsonpath.jsonpath(rsp_data, jsonpath_regex)  # 能提取到这位 [[XX], ...] 一个二维列表, 否则为False
        if target is False:
            pytest_check_res = pytest_check.is_false(fetch_res)
        elif target is True:
            pytest_check_res = pytest_check.is_true(fetch_res)
        else:
            logger.error(f"当断言类型为 exist时候, 期望的值只能为True或者False, 而您输入的为{target}")
            raise

        if not pytest_check_res:
            logger.error(
                f"期望使用 {jsonpath_regex} 表达式 去响应中 断言其对应存在性为 {target} , 但实际为 {pytest_check_res}")
            logger.error("被断言的响应体信息为  " + json.dumps(rsp_data, indent=2, ensure_ascii=False))
            return False
        else:
            logger.debug(
                f"期望使用 {jsonpath_regex} 表达式 去响应中 断言其对应存在性为 {target} , 期望和实际一致, 成功")
            return True

    else:  # 平常的值对象的比较, 即大小包含这些
        # 从响应体中取出被比较对象

        fetch_res = jsonpath.jsonpath(rsp_data, jsonpath_regex)
        if not fetch_res:
            logger.error(f"使用该jsonpath表达式不能从响应体中取得对应数据, 对应jsonpath表达式为{jsonpath_regex}")
            logger.error("被断言的响应体信息为  " + json.dumps(rsp_data, indent=2, ensure_ascii=False))
            raise
        else:
            compared_obj = fetch_res[0]
            # compared_obj = jsonpath.jsonpath(rsp_data, jsonpath_regex)[0]
        # 比较符的统一
        compare_type = get_unify_compare_symbol(compare_symbol)

        # 做实际比较
        cmp_res = compare_action(compared_obj, compare_type, target)
        logger.debug("单个断言::compared_obj::" + str(compared_obj))
        logger.debug("单个断言::compare_type::" + str(compare_type))
        logger.debug("单个断言::target      ::" + str(target))
        logger.info("断言结果cmp_res::" + str(cmp_res))
        return cmp_res


def check_json_all_expect(rsp_data, check):
    if check is None:
        return True

    # 判断check传进来的参数是不是二维列表, 并处理
    change_two_dimensional_flag = False
    for element in check:
        if not isinstance(element, list):
            change_two_dimensional_flag = True
            break
    if change_two_dimensional_flag:
        check = [check]

    # 依次对各个断言进行操作
    all_check_res = True
    for each_check in check:
        each_check = rebuild_check_expression(each_check)
        one_check_res = check_json_with_one_expect(rsp_data, each_check)
        if one_check_res is False:
            all_check_res = False
    return all_check_res



def rebuild_fetch_expression(self, expression):
    step_context = StepContext()
    rsp_field = step_context.rsp_field

    if len(expression) == 4:
        # 暂时不处理长度为 4 # TODO 待开发
        raise

    if len(expression) == 3:
        fetch_str = expression[2] # 3个长度的时候
        if "$." not in fetch_str:
            if rsp_field is not None:  # 存在rsp_field 的情况才去处理
                if fetch_str in rsp_field.keys():
                    field_info = rsp_field.get(fetch_str)
                    if "jsonpath" in field_info:
                        jsonpath_expression = field_info["jsonpath"]
                        expression[2] = jsonpath_expression

    return expression

def rebuild_check_expression(expression):
    step_context = StepContext()
    rsp_field = step_context.rsp_field

    if len(expression) == 4:
        # 暂时不处理长度为 4 # TODO 待开发
        raise

    if len(expression) == 3:
        check_str = expression[0]  # 3个长度的时候
        if "$." not in check_str:
            if rsp_field is not None: # 如果Api中定义了这个数据
                if check_str in rsp_field.keys():
                    field_info = rsp_field.get(check_str)
                    if "jsonpath" in field_info:
                        jsonpath_expression = field_info["jsonpath"]
                        expression[0] = jsonpath_expression

    return expression

def get_jsonpath_expression_from_rsp_field(key):
    """
    如果传入的不是 $. 开头的, 那么如果不是不同的key, 那就是 在rsp_field中有定义
    """

    key_res = None
    step_context = StepContext()
    rsp_field = step_context.rsp_field
    if key in rsp_field.keys():
        key_info = rsp_field[key]
        if "jsonpath" in key_info.keys():
            jsonpath_expression = key_info["jsonpath"]
            key_res = jsonpath_expression

    if key_res is not None:
        return key_res
    else:
        return key


__all__ = [
    "check_obj",  # 常用API
    "get_unify_compare_symbol",  # 判断断言的类型
    "compare_action",  # 断言函数
    "check_json_with_one_expect",
    "check_json_all_expect"
]
