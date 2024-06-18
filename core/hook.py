from core.logger import logger_init, logger_end
from common.ruoyi_logic import *
import json

"""
打包方法：
终端进入到 setup.py 文件路径下，执行打包命令：python setup.py sdist bdist_wheel
pip卸载插件包命令
pip安装插件包命令
备注:
pip install setuptools
pip install wheel
"""

case_file_path_dict = {}
logger = None

def pytest_collection_modifyitems(items):
    # print("items", items)
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
    pass

def pytest_collect_file(file_path, path, parent):
    print("pytest_collect_file 当前这个钩子函数不再使用")
    # print("file_path, path, parent", file_path, path, parent)
    # global case_file_path_dict
    # py_file_name = os.path.split(file_path)[1]  # test_add_user_998.py
    # case_file_path_dict[py_file_name] = str(file_path)

def pytest_runtest_logstart(nodeid, location):
    print("pytest_runtest_logstart", nodeid, location)
    global logger
    service_context = ServiceContext()
    base_path = service_context.base_path

    py_file_path = location[0]  # 即 以 ..cases 开头, 或者 cases 开头的文件路径
    # 因为在pycharm中执行 和 使用run_api_case来执行的调用过程不同,导致py_file_name信息不一致,需要做处理
    # run_api_case 场景: py_file_name ..\cases\api\process\architecture\new\test_process_architecture_add_001.py
    # 直接pycharm场景py_file_name test_process_architecture_add_001.py
    if ".." in py_file_path:
        py_file_path = py_file_path[2:]

    case_id = os.path.basename(py_file_path)[:-3]

    abs_file_path = os.path.join(base_path, py_file_path)
    logger = logger_init(abs_file_path)

    # 重置 业务上下文中的 restore_list 和 runtime_chain
    service_context = ServiceContext()
    service_context.reset_service_context()  # 需要再每个脚本的最开始处, 将业务的上下文信息清除掉, 因为连跑的时在同一个进程中的数据不会被清理
    service_context.case_id = case_id


def pytest_runtest_teardown(item, nextitem):
    """
    后置步骤: 打印相关日志
    """
    global logger
    logger.info("pytest_runtest_teardown")

    # ==========================================================   读取脚本上下文中的restore_list, 来做恢复操作
    service_context = ServiceContext()
    restore_list = service_context.restore_list

    restore_list.reverse()
    for restore in restore_list:
        if not restore:  # 如果是空的, 及时抛出异常问题, 让框架维护人去维护
            logger.error("restore_list不应该出现{}这种情况, 请及时定位排查")
            raise
        restore: dict
        # 取出 cur_restore_flag, 并从字典中去删除
        cur_restore_flag = restore["cur_restore_flag"]
        del restore["cur_restore_flag"]

        # 根据恢复的标记位 去恢复操作
        if cur_restore_flag:
            func_name, para_info = restore.popitem()
            if func_name in globals() and callable(globals()[func_name]):
                # 入参可能有多个, 需要遍历处理
                call_para = {}
                for para_name, para_value in para_info.items():
                    call_para.update({para_name: para_value})
                func = globals()[func_name]
                func(**call_para)

    # 更新运行时链条
    # 注意: teardown的后置过程中, 先执行的钩子函数, 在执行的业务脚本层编写的函数调用
    service_context.runtime_chain.append("script_end")
    logger.debug("service_context.runtime_chain 信息为:: " +
                 json.dumps(service_context.runtime_chain, indent=2, ensure_ascii=False))
    # ==========================================================   读取脚本上下文中的restore_list, 来做恢复操作

def pytest_runtest_logfinish(nodeid, location):
    print("pytest_runtest_logfinish", nodeid, location)
    global logger
    logger_end()
    pass