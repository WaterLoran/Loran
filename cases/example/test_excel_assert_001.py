# coding: utf-8
from common.ruoyi_logic import *

"""
excel断言的示例脚本
"""

class TestExcelAssert001(object):
    def setup_method(self):
        pass


    @allure.title("Excel断言功能示例")
    def test_excel_assert_001(self):

        # Precondition operation:
        #按照测试目的自行构造

        # Procedure:
        #[1]正向操作

        # Expected results:
        #[1]操作成功

        # 前后筛选后的行 的集合 是一样的
        check_excel(
            {
                "file": "excel断言示例所用.xlsx",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    {
                        "column_name": "人员名称",  # column_index暂不支持
                        "column_value": "张三"  # 支持传入列表, 即支持多个数值
                    },
                    {
                        "column_name": "人员账号",
                        "column_value": 88880001
                    },
                ],
                "assert_type": "equal",  # 提供集合类型的比较关系, 等于, 不等于, 包含, 不包含, 属于, 不属于
                "target": [
                    {
                        "column_name": "功能角色",
                        "column_value": "销售工程师"  # # 支持传入列表, 即支持多个数值
                    },
                    {
                        "column_name": "业务范围",
                        "column_value": "业务范围A"
                    },
                    {
                        "column_name": "年龄",
                        "column_value": 25
                    },
                ]
            }
        )

        # 判断方式使用 子集判断的方式  # <=表示 左边的是右边的子集
        check_excel(
            {
                "file": "excel断言示例所用.xlsx",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    {
                        "column_name": "人员名称",  # column_index暂不支持
                        "column_value": "张三"  # 支持传入列表, 即支持多个数值
                    },
                    {
                        "column_name": "人员账号",
                        "column_value": 88880001
                    },
                ],
                "assert_type": "<=",  # <=表示 左边的是右边的子集
                "target": [
                    {
                        "column_name": "年龄",
                        "column_value": 25  # # 支持传入列表, 即支持多个数值
                    },
                ]
            }
        )

        # 判断方式使用 子集判断的方式  # => 表示 右边是左边的子集
        check_excel(
            {
                "file": "excel断言示例所用.xlsx",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    {
                        "column_name": "年龄",
                        "column_value": 25  # # 支持传入列表, 即支持多个数值
                    },
                ],
                "assert_type": "=>",  # <=表示 左边的是右边的子集
                "target": [
                    {
                        "column_name": "人员名称",  # column_index暂不支持
                        "column_value": "张三"  # 支持传入列表, 即支持多个数值
                    },
                    {
                        "column_name": "人员账号",
                        "column_value": 88880001
                    },
                ]
            }
        )

        # 直接断言数量 --> 名字为张三
        check_excel(
            {
                "file": "excel断言示例所用.xlsx",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    {
                        "column_name": "人员名称",  # column_index暂不支持
                        "column_value": "张三"  # 支持传入列表, 即支持多个数值
                    },
                    {
                        "column_name": "人员账号",
                        "column_value": 88880001
                    },
                ],
                "assert_type": "equal",  # 提供集合类型的比较关系, 等于, 不等于, 包含, 不包含, 属于, 不属于
                "target": 1
            }
        )

        # 直接断言数量 --> 名字为张三
        check_excel(
            {
                "file": "excel断言示例所用.xlsx",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    {
                        "column_name": "年龄",  # column_index暂不支持
                        "column_value": 25  # 支持传入列表, 即支持多个数值
                    },
                ],
                "assert_type": "equal",  # 提供集合类型的比较关系, 等于, 不等于, 包含, 不包含, 属于, 不属于
                "target": 2
            }
        )

        # 断言集合 相等
        check_excel(
            {
                "file": "excel断言示例所用.xlsx",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    {
                        "column_name": "年龄",  # column_index暂不支持
                        "column_value": 25  # 支持传入列表, 即支持多个数值
                    },
                ],
                "assert_type": "equal",  # 提供集合类型的比较关系, 等于, 不等于, 包含, 不包含, 属于, 不属于
                "target": [
                    {
                        "column_name": "年龄",  # column_index暂不支持
                        "column_value": 25  # 支持传入列表, 即支持多个数值
                    },
                ],
            }
        )

        # 使用 condition 中的元素为列表的使用场景 的demo (简化的写法)
        check_excel(
            {
                "file": "excel断言示例所用.xlsx",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    ["人员名称", "张三"],
                    ["人员账号", 88880001],
                ],
                "assert_type": "equal",  # 提供集合类型的比较关系, 等于, 不等于, 包含, 不包含, 属于, 不属于
                "target": 1
            }
        )

        # 支持对 xls格式的excel文件进行断言
        check_excel(
            {
                "file": "excel断言示例所用_xls格式.xls",
                "sheet": "Sheet1",  # 如果不传, 则默认为Sheet1
                "condition": [
                    ["人员名称", "张三"],
                    ["人员账号", 88880001],
                ],
                "assert_type": "equal",  # 提供集合类型的比较关系, 等于, 不等于, 包含, 不包含, 属于, 不属于
                "target": 1
            }
        )

    def teardown_method(self):
        pass
