# coding=utf8
from common.ruoyi_logic import *

# 新增支持 fetch表达式为3位的时候, 使用rsp_field来重建出完整的 表达式
class TestUseRspField001:
    def setup_method(self):
        pass

    def test_use_rsp_field_001(self):
        reg = register({
            "user_id": None,
            "user_id2": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "hello22"
        add_user(
            userName=var_name, nickName=var_name, password=var_name,
            # check=[
            #     ["$.msg", "eq", "操作成功"],
            #     ["$.code", "==", 200],
            #     ["msg", "eq", "操作成功"]  # 此处就是使用了 rsp_field 来重建获取表达式来的
            # ],
        )

        # 查看用户
        lst_user(
            fetch=[
                [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
                [reg, "user_id2", f"$.rows[?(@.userName=='{var_name}')].userId"],
                [reg, "msg", "msg"]  # 此处使用了rsp_field预定义的jsonpath表达式
            ],
            check=[
                # [f"$.rows[?(@.userName=='{var_name}')].nickName", "eq", var_name],
                ["msg", "eq", "查询成功"], # 此处使用了rsp_field预定义的jsonpath表达式
            ]
        )

        print("reg.msg", reg.msg)

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
