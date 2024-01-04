from common.ruoyi_logic import *
from core.event import Event

class TestLoopToSuccess:
    def setup(self):
        pass

    def test_loop_to_success(self):
        reg = register({
            "user_id": None,
            "user_id2": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "hello22"
        add_user(
            userName=var_name, nickName=var_name, password=var_name,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )

        # 查看用户
        lst_user(
            fetch=[
                [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
                [reg, "user_id2", f"$.rows[?(@.userName=='{var_name}')].userId"],
            ],
            check=[f"$.rows[?(@.userName=='{var_name}')].nickName", "eq", var_name]
        )

        @Event.background(60)
        def b_func():
            return lst_user(
                fetch=[
                    [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
                    [reg, "user_id2", f"$.rows[?(@.userName=='{var_name}')].userId"],
                ],
                check=[f"$.rows[?(@.userName=='{var_name}')].nickName", "eq", var_name]
            )
        b_func()

        # 验证这个函数的使用的时候, 需要上去环境将  hello22的用户的昵称改成MIKE
        @Event.loop_to_success(3)
        def t_func():
            return lst_user(
                fetch=[
                    [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
                    [reg, "user_id2", f"$.rows[?(@.userName=='{var_name}')].userId"],
                ],
                # check=[f"$.rows[?(@.userName=='{var_name}')].nickName", "eq", "MIKE"]
            )
        t_func()



    def teardown(self):
        # 删除用户
        rmv_user(
            userId=self.reg.user_id,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )
