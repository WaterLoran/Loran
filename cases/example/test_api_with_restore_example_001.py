# coding=utf8
from common.ruoyi_logic import *


class TestApiWithRestoreExample001:
    """
    """
    def setup_method(self):
        pass

    def test_api_with_restore_example_001(self):
        reg = register({
            "user_id": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "api_with_restore_example_001"
        add_user(
            userName=var_name, nickName=var_name, password=var_name,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.msg", "eq", "操作成功"],
            ]
        )

        # 这个关键字就带有restore, 即查看后会在后置中去清除数据,
        # 实际上使用的场景为, add_xxx 添加数据之后, 会通过设置restore来在后置中清除数据
        # 但是若依管理系统中的ADD数据接口, 都不会返回相关的ID信息, 所以这里只能使用这个LST接口来做相关例子的举例
        lst_user_wtih_restore(
            userName=var_name,
            restore=True
        )

    def teardown_method(self):
        pass
