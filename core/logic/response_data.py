import copy
import pytest_check
from core.logger import LoggerManager
from core.check import *
from core.fetch import *

logger = LoggerManager().get_logger("main")


class ResponseData:
    def __init__(self):
        pass

    def rsp_fetch_all_value(self, rsp_data, fetch):
        return fetch_json_all_value(rsp_data, fetch)

    def check_all_expect(self, rsp_data, check):
        return check_json_all_expect(rsp_data, check)

    def check_api_default_expect(self, req_data, rsp_data, rsp_check, check):
        # 将rsp_check 转换成  类似于  check = [Var_a, "==", "target_value"]
        # 递归rsp_check, 获得信息
        # 然后再拿这个表达式去做断言
        if not rsp_check:
            return True

        def judge_expression_type(expression):
            expression_type = "string"
            try:
                if "$." in expression:
                    expression_type = "regex"
            except:
                pass
            return expression_type

        pytest_check_cache = []

        def traverse_json(check_data, real_rsp, path):
            nonlocal pytest_check_cache

            if isinstance(check_data, tuple):
                logger.error("业务脚本层的主动断言传入的数据格式不能为元组, 期望为列表, 并且列表中有三个元素")
                raise
            for key, value in check_data.items():
                if isinstance(value, dict):  # 是一个字典
                    t_path = copy.deepcopy(path)
                    t_path.append(key)
                    if key not in real_rsp.keys():
                        logger.error("真实响应中没有该字段, 请检查API默认断言的数据-real_rsp_has_no_such_field")
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
                            logger.error("列表里面只期望有字典, 其他场景是非法的, 或者需要进一步去封装处理")
                            raise
                    pass
                else:  # 表示这就是普通的键值对了, 并且他的值value, 有坑你就是普通的字符串, 或有有可能是键值对来的
                    # 判断是普通的字符串, 还是正则表达式
                    # expression_type = XX_funx()
                    t_path = copy.deepcopy(path)
                    # expression_type = "string"
                    expression_type = judge_expression_type(value)
                    if expression_type == "string":
                        logger.debug("取值的表达式类型为string")
                        check_type = "string"
                        except_obj = value
                        if key not in real_rsp.keys():
                            print("real_rsp_has_no_such_field")
                            logger.error("real_rsp_has_no_such_field")
                            raise
                    elif expression_type == "regex":  # 这里为正则表达式的时候, 设计上, 需要使用这个正则表达式去请求体中去获得数据做为期望值
                        # 第一步, 使用jsonpath表达式去请求体中获得想响应的数据, 注意: req_json, data
                        except_obj = jsonpath.jsonpath(req_data, value)[0]  # value就是正则表达式, 比如可能为$.nickName
                        check_type = "regex"
                        # 第二步, 那就跟string类型的比较大差不差
                        pass
                    else:
                        raise

                    ## 更新数据到pytest_check
                    target_obj = real_rsp[key]
                    check_obj = {
                        "check_type": check_type,
                        "except_obj": except_obj,
                        "target_obj": target_obj,
                        "path": t_path
                    }
                    pytest_check_cache.append(check_obj)

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

        default_check_res = True
        if rsp_data["code"] != 200 and check is not None:  # check是主动断言的入参, 响应失败并且由主动断言时, 不去做默认断言, 因为这个时候实际为用户在做异常接口测试
            logger.warning("此步骤中业务脚本层check信息不为None,且响应状态码为失败, 不做API数据层的预定义断言")
            logger.debug(f"check:: {check}")
        else:  # 其他情况都要做断言
            for check_obj in pytest_check_cache:
                check_type = check_obj["check_type"]
                except_obj = check_obj["except_obj"]
                target_obj = check_obj["target_obj"]
                path = check_obj["path"]

                logger.debug("需要API默认断言的总数量为" + str(len(pytest_check_cache)))
                logger.info(">>>>>>>>>>>>>>>>  对单个API层预定义的检查项做断言-开始\n")

                logger.debug("断言的类型为{}".format(check_type))
                logger.debug("预定义期望的路径为{}".format(path))

                except_debug_str = "API数据层预定义的期望except_obj为{}, 数据类型为{}".format((except_obj),
                                                                                              str(type(except_obj)))
                logger.debug(except_debug_str)
                target_debug_str = "实际的响应信息的target_obj为{}, 数据类型为{}".format((target_obj),
                                                                                         str(type(target_obj)))
                logger.debug(target_debug_str)
                pytest_check_result = pytest_check.equal(except_obj, target_obj)
                if not pytest_check_result:
                    default_check_res = False
                    logger.error("APi数据层预定义的断言结果为假  ==>  0  <== False ==> 假 <==")
                logger.info("<<<<<<<<<<<<<<<<  对单个API层预定义的检查项做断言-结束\n")
            return default_check_res
