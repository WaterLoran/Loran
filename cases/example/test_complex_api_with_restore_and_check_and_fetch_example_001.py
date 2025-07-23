# coding=utf8
from common.ruoyi_logic import *


class TestComplexApiWithRestoreAndCheckAndFetchExample001:
    """
    """
    def setup_method(self):
        pass

    def test_complex_api_with_restore_and_check_and_fetch_example_001(self):
        reg = register({
            "user_id": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "restore_check_fetch_001"
        add_user_complex(
            userName=var_name, nickName=var_name, password=var_name,
            add_check=[  # 这个复合逻辑也可以传入单个断言, 但可能不常用
                ["$.code", "eq", 200],
                ["$.msg", "eq", "操作成功"],
            ],
            lst_check=[
                ["$.code", "eq", 200],
                ["$.msg", "eq", "查询成功"],
                [f"$.rows[?(@.userName=='{var_name}')].nickName2", "exist", False],
                [f"$.rows[?(@.userName=='{var_name}')].nickName", "exist", True],
            ],
            # 第三个参数即为 复合关键字中的变量名, 可以通过传入fetch来获取fetch到的信息,
            # 但需要在符合logic中先fetch出来, 通常情况下不会单独fetch
            fetch=[reg, "user_id", "user_id"],
            restore=True
        )

        print("==== reg.user_id", reg.user_id)  # 这里表示确实可以fetch到

    def teardown_method(self):
        pass
