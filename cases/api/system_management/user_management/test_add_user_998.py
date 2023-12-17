from common.ruoyi_logic import *
from logger_fixture import logger_fixture


class TestAddUser997:
    def setup_class(self):
        pass

    # @logger_fixture()
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
            ]
        )

        # 查看用户
        lst_user(
            fetch=[
                [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
                [reg, "user_id2", f"$.rows[?(@.userName=='{var_name}')].userId"],
            ]
        )

        # 删除用户
        rmv_user(
            userId=self.reg.user_id,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ]
        )

    def teardown_class(self):

        pass
