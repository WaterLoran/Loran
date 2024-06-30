# -*- coding:utf8 -*-
import os
import argparse
import platform
import pytest


"""
提供的功能
1. 可选根据关键字去增量选择待执行脚本
2. 可选根据关键字去增量选择待执行脚本
"""

if __name__ == '__main__':

    base_path = os.getcwd()

    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='只执行匹配关键字的用例，会匹配文件名、类名、方法名', type=str)
    parser.add_argument('-d', '--dir', help='指定要测试的目录', type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试', type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0', type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0', type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0', type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    args = parser.parse_args()


    # 执行pytest前的参数准备
    if platform.system() == "Windows":
        pytest_execute_params = ['-r', "3", '-v', '--alluredir', r'.\output\allure_result', '--clean-alluredir']


    # 判断目录参数
    dir = 'cases/api/'
    if args.dir:
        dir = args.dir

    # 判断关键字参数
    if args.keyword:
        pytest_execute_params.append('-k')
        pytest_execute_params.append(args.keyword)

    # 判断markexpr参数
    if args.markexpr:
        pytest_execute_params.append('-m')
        pytest_execute_params.append(args.markexpr)

    # 判断是否输出日志
    if args.capture:
        if int(args.capture):
            pytest_execute_params.append('-s')

    # 判断是否失败重跑
    if args.reruns:
        if int(args.reruns):
            pytest_execute_params.append('--reruns')
            pytest_execute_params.append(args.reruns)

    # 判断是否只运行上一次失败的用例
    if args.lf:
        if int(args.lf):
            pytest_execute_params.append('--lf')

    # 判断是否清空已有测试结果
    if args.clr:
        if int(args.clr):
            pytest_execute_params.append('--clean-alluredir')
    pytest_execute_params.append(dir)

    try:
        print("pytest_execute_params", pytest_execute_params)
        exit_code = pytest.main(pytest_execute_params)
        print("自动化框架连跑结果值exit_code", exit_code)

        if platform.system() == "Windows":
            allure_result_path = r"E:\Develop\RuoYiTest\output\allure_result"
            allure_report_path = r"E:\Develop\RuoYiTest\output\allure_report"
            os.system(f"allure generate {allure_result_path} -o {allure_report_path} --clean")
        #     # TODO 拉起进程前, 需要杀掉allure的进程, window情况直接手工点击 output下的allure_report下的index.html 即可
        #     os.system(f"allure open -h 127.0.0.1 -p 8078 {allure_report_path}")
    except:
        pass
