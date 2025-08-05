# coding=utf8
from common.ruoyi_logic import *

# 新增支持 fetch表达式为3位的时候, 使用rsp_field来重建出完整的 表达式
class TestDataDepend001:
    def setup_method(self):
        pass

    def test_use_data_depend_001(self):
        reg = register({
            "user_id": None,
            "user_id2": None,
        })
        self.reg = reg

        department_name = "autotest_department"
        add_department(
            deptName=department_name
        )

        lst_department(
            fetch=[
                [reg, "department_data", f"$.data[?(@.deptName=='{department_name}')]"],
                [reg, "department_id", f"$.data[?(@.deptName=='{department_name}')].deptId"]
            ]
        )

        # 添加用户
        var_name = "use_data_depend_001"
        add_user(
            userName=var_name, # 这个字段将会使用req_field中定义的信息
            nickName=var_name,
            password=var_name, # 这个字段将会使用req_field中定义的信息
        )

        # 查看用户
        lst_user(
            fetch=[
                [reg, "user_data", f"$.rows[?(@.userName=='{var_name}')]"],
                [reg, "user_id", f"$.rows[?(@.userName=='{var_name}')].userId"],
            ],
        )

        mod_user(
            req_json=reg.user_data,  # 这里使用了 req_json 即直接去上级的信息作为本级的请求体
            dept=reg.department_data,
            deptId=reg.department_id
        )

        print()

    def teardown_method(self):
        # 删除用户
        rmv_user(
            userId=self.reg.user_id,
            check=[
                ["$.msg", "eq", "操作成功"],
                ["$.code", "==", 200],
            ],
        )

        rmv_department(
            departmentId=self.reg.department_id,
        )
        pass
