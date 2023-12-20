import os
from .logger import logger_init, logger_end

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
    print("file_path, path, parent", file_path, path, parent)
    global case_file_path_dict
    py_file_name = os.path.split(file_path)[1]  # test_add_user_998.py
    case_file_path_dict[py_file_name] = str(file_path)
    # case_file_path_dict = {
    #     "test_add_user_998.py": r"E:\Develop\RuoYiTest\cases\api\system_management\user_management\test_add_user_998.py"
    # }


def pytest_runtest_logstart(nodeid, location):
    print("pytest_runtest_logstart", nodeid, location)
    global logger
    global case_file_path_dict
    py_file_name = location[0]

    # 因为在pycharm中执行 和 使用run_api_case来执行的调用过程不同,导致py_file_name信息不一致,需要做处理
    # run_api_case 场景: py_file_name ..\cases\api\process\architecture\new\test_process_architecture_add_001.py
    # 直接pycharm场景py_file_name test_process_architecture_add_001.py
    if "\\" in py_file_name or "/" in py_file_name:
        py_file_name = os.path.split(py_file_name)[1]

    abs_file_path = case_file_path_dict[py_file_name]
    logger = logger_init(abs_file_path)
    pass


def pytest_runtest_logfinish(nodeid, location):
    print("pytest_runtest_logfinish", nodeid, location)
    global logger
    logger_end()
    pass