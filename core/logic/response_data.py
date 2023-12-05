import jsonpath
import pytest_check


class ResponseData:
    def __init__(self):
        pass

    def _fetch_one_value(self, rsp_data, each_fetch):

        # 做一个提取信息的操作
        print("each_fetch", each_fetch)
        reg = each_fetch[0]
        reg_key = each_fetch[1]
        jsonpath_regex = each_fetch[2]

        target_value = jsonpath.jsonpath(rsp_data, jsonpath_regex)[0]
        print("target_value", target_value)

        reg[reg_key] = target_value
        print("reg[reg_key]", reg[reg_key])

    def fetch_all_value(self, rsp_data, fetch):
        if fetch is None:
            return

        # 判断入参的格式, 然后统一一下格式
        # 判断check传进来的参数是不是二维列表, 并处理
        change_two_dimensional_flag = False
        for element in fetch:
            if not isinstance(element, list):
                change_two_dimensional_flag = True
                break
        if change_two_dimensional_flag:
            fetch = [fetch]

        for each_fetch in fetch:
            self._fetch_one_value(rsp_data, each_fetch)



    def get_unify_compare_symbol(self, symbol):
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
        raise   # TODO 都没有在里面, 需要抛出异常和定位信息

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

    def _check_one_expect(self, rsp_data, each_check):
        jsonpath_regex = each_check[0]
        compare_symbol = each_check[1]
        target = each_check[2]

        # 从响应体中取出被比较对象

        compared_obj = jsonpath.jsonpath(rsp_data, jsonpath_regex)[0]  # TODO, 需要做一些判断, 如果查出来有两个则出UI长和定位信息
        # 比较符的统一
        compare_type = self.get_unify_compare_symbol(compare_symbol)

        # 做实际比较
        cmp_res = self.compare_action(compared_obj, compare_type, target)
        print("断言结果cmp_res", cmp_res)
        # TODO 如果断言结果为假, 那么需要打印相关的信息, 日志
        pass


    def check_all_expect(self, rsp_data, check):

        if check is None:
            return

        # 判断check传进来的参数是不是二维列表, 并处理
        change_two_dimensional_flag = False
        for element in check:
            if not isinstance(element, list):
                change_two_dimensional_flag = True
                break
        if change_two_dimensional_flag:
            check = [check]

        # 依次对各个断言进行操作
        for each_check in check:
            self._check_one_expect(rsp_data, each_check)
        pass

    def check_api_default_expect(self, rsp_data, rsp_check):
        pass

