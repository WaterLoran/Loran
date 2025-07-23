# coding=utf8
from common.ruoyi_logic import *


class TestAddUser998:
    def setup_method(self):
        pass

    def test_add_user_998(self):
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
                ["msg", "eq", "操作成功"]
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

        print("config==>", config.user.autotest)


    def teardown_method(self):
        # 删除用户
        rmv_user(
            userId=self.reg.user_id,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )

        pass
