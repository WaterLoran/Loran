# -*- coding: utf8 -*-
# !/usr/bin/python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

long_description ="""Python栈-自动化测试框架
前华为测试开发工程师, 充分借鉴httprunner框架的设计优点 和 华为某大部门的测试框架的规范,
首创基于aop实现的面向切面编程描述式的python语法框架. 超级容易上手, 自动化最优实践!!

特点是, 易读易维护, 我希望这个框架的设计思路能够统一未来新增的自动化框架市场. 当前该框架有其直白高效的范式, 数据和逻辑高度解耦, 
核心功能有日志, 报告, 断言, 提取信息, 多次重试, 插件功能有执行mysql命令, excel断言, 脚本连跑执行入口等.
"""

setup(
    name='loran',  # 虽然这个名字为RuoyiTest, 但是 这个库还是以Loran来命名
    version='1.0',
    author='WaterLoran',
    author_email='1696746432@qq.com',
    url='https://github.com/WaterLoran/RuoYiTest',
    download_url="http://pypi.python.org/pypi/easydict/",
    description="Core Paradigm of Automation Framework",
    # long_description=open(os.path.join(here, 'README.rst')).read() + '\n\n' +
    #                  open(os.path.join(here, 'CHANGES')).read(),
    long_description=long_description,
    license='LGPL-3.0',
    install_requires=[
        "jsonschema==4.22.0",
        "pandas==2.2.2",
        "pytest-check==2.2.2",
        "openpyxl==3.1.2",
        "easydict==1.11",
        "colorlog==6.8.0",
        "allure-pytest==2.13.2",
        "seleniumbase==4.22.5",
        "xlrd==2.0.1",
        "fire==0.6.0",
        "PyMySQL==1.1.1",
        "jsonpath==0.82.2"
    ],
    packages=find_packages(include=['loran', 'loran.*'], exclude=['common', 'common.*']),
    # 自动查找包, 当前这种写法, 会导入多余的目录common
    # package_dir={'': '.'},          # 指定包目录
    package_data={
        'loran': [
            'loran/scaffold/cases/*',
            'loran/scaffold/files/*',
            'loran/scaffold/config/*',
        ],
    },
    # include loran/scaffold/files/*
    # include loran/scaffold/config/*
    # include loran/scaffold/cases/*
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'loran = loran.cmdline:main'  # loran 即为命令名称
        ]
    },
    keywords=['Test', "AutoTest", "automated testing", "测试", "自动化测试"],
    classifiers=[
        'Topic :: Software Development :: Testing',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.9'],
)

# 上传包到 Pypi的命令
# twine upload dist/*
