# -*- coding: utf8 -*-
# !/usr/bin/python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='LoranTest',  # 虽然这个名字为RuoyiTest, 但是 这个库还是以LoranTest来命名
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
        "seleniumbase==4.22.5"
    ],
    packages=find_packages(include=['core', 'core.*'], exclude=['common', 'common.*']),  # 自动查找包, 当前这种写法, 会导入多余的目录common
    # package_dir={'': '.'},          # 指定包目录
    py_modules=[''],
    include_package_data=True,
    zip_safe=False,
    keywords=['Test', "AutoTest", "automated testing", "测试", "自动化测试"],
    classifiers=['Topic :: Autotest',
                 'Natural Language :: Chinese (Simplified)',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Development Status :: 4 - Beta',
                 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                 'Programming Language :: Python :: 3.9.7'],
)

#  打包命令: python setup.py sdist bdist_wheel
# 然后将文件覆盖到D:\EprosTest\venv\Scripts目录下, 然后执行pip安装

# MANIFEST.in  用于描述, 所要排除的目录, 并且要同时结合packages=find_packages(include=['core', 'core.*'], exclude=['common', 'common.*'])
