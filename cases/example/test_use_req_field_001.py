# coding=utf8
from common.ruoyi_logic import *

# 新增支持 fetch表达式为3位的时候, 使用rsp_field来重建出完整的 表达式
class TestUseReqField001:
    def setup_method(self):
        pass

    def test_use_req_field_001(self):
        reg = register({
            "user_id": None,
            "user_id2": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "hello22"
        nickName = "nickName"
        password = "password"
        add_user(
            userName=var_name, # 这个字段将会使用req_field中定义的信息
            nickName=nickName,
            password=password, # 这个字段将会使用req_field中定义的信息
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
                ["msg", "eq", "操作成功"]  # 此处就是使用了 rsp_field 来重建获取表达式来的
            ],
        )

        # 查看用户
        lst_user(
            fetch=[
                [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
            ],
        )

        lst_user_by_id(
            userId=reg.user_id,
            fetch=[reg, "user_data", "$.data"]
        )

        mod_user(
            req_json=reg.user_data,  # 这里使用了 req_json 即直接去上级的信息作为本级的请求体
            remark="一些备注信息"
        )

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
