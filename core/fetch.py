import jsonpath
from core.logger.logger_interface import logger


def fetch_json_one_value(rsp_data, each_fetch):
    # 做一个提取信息的操作
    logger.debug(f"each_fetch:: {each_fetch} ")
    reg = each_fetch[0]
    reg_key = each_fetch[1]
    jsonpath_regex = each_fetch[2]

    target_value = jsonpath.jsonpath(rsp_data, jsonpath_regex)[0]
    logger.debug(f"提取出来的目标信息::target_value:: {target_value} ")

    reg[reg_key] = target_value


def fetch_json_all_value(rsp_data, fetch):
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
        fetch_json_one_value(rsp_data, each_fetch)