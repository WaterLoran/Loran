# -*- coding: utf8 -*-
# !/usr/bin/python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

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
    long_description=open('readme.md', encoding="utf-8").read(),
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
    packages=find_packages(include=['loran', 'loran.*'], exclude=['common', 'common.*']),  # 自动查找包, 当前这种写法, 会导入多余的目录common
    # package_dir={'': '.'},          # 指定包目录
    package_data={
        'loran': [
            'loran/scaffold/cases/*',
            'loran/scaffold/files/*',
            'loran/scaffold/config/*',
        ],
    },
    py_modules=[''],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'loran = loran.cmdline:main'  # loran 即为命令名称
        ]
    },
    keywords=['Test', "AutoTest", "automated testing", "测试", "自动化测试"],
    classifiers=['Topic :: Autotest',
                 'Natural Language :: Chinese (Simplified)',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Development Status :: 4 - Beta',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Programming Language :: Python :: 3.9.7'],
)
# 先安装 setuptools, wheel 这两个库, 然后, 在setup.py 这个文件夹目录下,
# 启动控制台来执行 打包命令, 然后再dist目录找到 whl结尾的文件去安装
# pip install setuptools
# pip install wheel
#  打包命令: python setup.py sdist bdist_wheel
# 然后将文件覆盖到D:\EprosTest\venv\Scripts目录下, 然后执行pip安装

# MANIFEST.in  用于描述, 所要排除的目录, 并且要同时结合packages=find_packages(include=['loran', 'loran.*'], exclude=['common', 'common.*'])
