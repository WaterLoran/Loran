import copy

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

    def check_api_default_expect(self, rsp_data, rsp_check, check):
        # 将rsp_check 转换成  类似于  check = [Var_a, "==", "target_value"]
            # 递归rsp_check, 获得信息
        # 然后再拿这个表达式去做断言
        if not rsp_check:
            return

        pytest_check_cache = []
        def traverse_json(check_data, real_rsp, path):
            nonlocal pytest_check_cache

            if isinstance(check_data, tuple):
                print("这里不能是元组")
                raise
            for key, value in check_data.items():
                if isinstance(value, dict):
                    t_path = copy.deepcopy(path)
                    t_path.append(key)
                    if key not in real_rsp.keys():
                        print("real_rsp_has_no_such_field")
                        raise
                    traverse_json(value, real_rsp[key], t_path)
                elif isinstance(value, list):  # 有可能这个就是根节点, 这个就是要比较的数据
                    for i in range(len(value)):
                        item = value[i]
                        if isinstance(item, dict):
                            t_path = copy.deepcopy(path)
                            t_path.append(key)
                            traverse_json(item, real_rsp[i], t_path)
                        else:
                            print("列表里面只期望有字典, 其他场景是非法的, 或者需要进一步去封装处理")
                            raise
                    pass
                else:  # 表示这就是普通的键值对了, 并且他的值value, 有坑你就是普通的字符串, 或有有可能是键值对来的
                    # 判断是普通的字符串, 还是正则表达式
                    # expression_type = XX_funx()
                    t_path = copy.deepcopy(path)
                    expression_type = "string"
                    if expression_type == "string":
                        print("根据api层预定义的单个check信息做断言")
                        print("取值的表达式类型为string")
                        check_type = "string"
                        except_obj = value
                        if key not in real_rsp.keys():
                            print("real_rsp_has_no_such_field")
                            raise
                        target_obj = real_rsp[key]
                        check_obj = {
                            "check_type": check_type,
                            "except_obj": except_obj,
                            "target_obj": target_obj,
                            "path": t_path
                        }
                        pytest_check_cache.append(check_obj)
                    elif expression_type == "regex":  # 这里为正则表达式的时候, 设计上, 需要使用这个正则表达式去请求体中去获得数据做为期望值
                        pass
                    else:
                        raise

        # 如果该请求是成功的, 我们才去做默认断言, 如果是失败的话, 就不去做默认断言
        # 请求成功, 主动断言有, 默认断言有    DO
        # 请求成功, 主动断言有, 默认断言无
        # 请求成功, 主动断言无, 默认断言有    DO
        # 请求成功, 主动断言无, 默认断言无
        # 请求失败, 主动断言有, 默认断言有    不做默认断言
        # 请求失败, 主动断言有, 默认断言无    不做默认断言
        # 请求失败, 主动断言无, 默认断言有    Do
        # 请求失败, 主动断言无, 默认断言无
        traverse_json(rsp_check, rsp_data, check)

        if rsp_data["code"] != 200 and check is not None:  # check是主动断言的入参, 响应失败并且由主动断言时, 不去做默认断言, 因为这个时候实际为用户在做异常接口测试
            print("此步骤中业务脚本层check信息不为None,且响应状态码为失败, 不做API数据层的预定义断言")
        else:  # 其他情况都要做断言
            print("========  开始根据API数据层定义的rsp_check做自动断言  ========\n")
            for check_obj in pytest_check_cache:
                check_type = check_obj["check_type"]
                except_obj = check_obj["except_obj"]
                target_obj = check_obj["target_obj"]
                path = check_obj["path"]

                print("需要API默认断言的总数量为" + str(len(pytest_check_cache)))
                print("====  开始对单个API层预定义的检查项做断言  ====")

                print("断言的类型为{}".format(check_type))
                print("预定义期望的路径为{}".format(path))

                except_debug_str = "API数据层预定义的期望except_obj为{}, 数据类型为{}".format((except_obj),
                                                                                              str(type(except_obj)))
                print(except_debug_str)
                target_debug_str = "实际的响应信息的target_obj为{}, 数据类型为{}".format((target_obj),
                                                                                         str(type(target_obj)))
                print(target_debug_str)
                pytest_check_result = pytest_check.equal(except_obj, target_obj)
                if not pytest_check_result:
                    print("APi数据层预定义的断言结果为假  ==>  0  <== False ==> 假 <==")
                print("====  结束对单个API层预定义的检查项做断言  ====\n")
            print("========  结束根据API数据层定义的rsp_check做自动断言  ========\n")


