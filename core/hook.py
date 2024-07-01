from core.logger import logger_init, logger_end
from common.ruoyi_logic import *
import json

logger = None
py_file_2_abs_path = {}


def pytest_collect_file(file_path, path, parent):
    # pycharm执行的时候, 会跳过这个钩子函数, 所以, 不使用这个钩子函数了
    print("pytest_collect_file 当前这个钩子函数不再使用")


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    global py_file_2_abs_path
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

        # 汇聚 py文件名(basename带.py) 和 绝对路径的映射关系
        basename = item.fspath.basename
        strpath = item.fspath.strpath
        py_file_2_abs_path[basename] = strpath


def pytest_runtest_logstart(nodeid, location):
    print("pytest_runtest_logstart", nodeid, location)
    global logger
    global py_file_abs_path

    basename = location[0]  # 即 以 ..cases 开头, 或者 cases 开头的文件路径
    basename = os.path.basename(basename)  # 非安装 pycharm执行是 case开头的, 需要再取一次basename
    case_id = os.path.basename(basename)[:-3]

    # 因为在pycharm中执行 和 使用run_api_case来执行的调用过程不同,导致py_file_name信息不一致,需要做处理
    # run_api_case 场景: py_file_name ..\cases\api\process\architecture\new\test_process_architecture_add_001.py
    # 直接pycharm场景py_file_name test_process_architecture_add_001.py
    # 现在直接从 pytest_collection_modifyitems 中收集好的数据去提取想信息

    # 注册日志器
    py_file_abs_path = py_file_2_abs_path[basename]
    logger = logger_init(py_file_abs_path)

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
