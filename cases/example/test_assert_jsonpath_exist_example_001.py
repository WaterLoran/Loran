# coding=utf8
from common.ruoyi_logic import *
from core.event import Event


class TestAssertJsonpathExistExample001:
    """
    有时候, 仅仅需要断言某个jsonpath表达式在响应中能够取值成功, 而不需要取出具体的值,
    现在这里提供这种想写法, 能够让逻辑的表达更加清晰
    """
    def setup(self):
        pass

    def test_assert_jsonpath_exist_example_001(self):
        reg = register({
            "user_id": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "hello22"
        add_user(
            userName=var_name, nickName=var_name, password=var_name,
            check=[
                ["$.code", "exist", True],
            ],
        )

        # 查看用户
        lst_user(
            fetch=[
                [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
            ],
            check=[
                [f"$.rows[?(@.userName=='{var_name}')].nickName", "eq", var_name],
                [f"$.rows[?(@.userName=='{var_name}')].nickName2", "exist", False],
                [f"$.rows[?(@.userName=='{var_name}')].nickName", "exist", True],
            ]
        )


    def teardown(self):
        # 删除用户
        rmv_user(
            userId=self.reg.user_id,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )

