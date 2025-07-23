# coding=utf8
from common.ruoyi_logic import *


class TestRoleManagementLifecycle001:
    def setup_method(self):
        pass

    def test_role_management_lifecycle_001(self):
        reg = register({
            "role_id": None,
        })
        self.reg = reg

        # 添加角色
        role_name = "role_management_lifecycle_001"
        add_role(
            roleName=role_name, roleKey=role_name, roleSort=6,
            menuIds=[
                1,
                100,
                1000
            ],
            remark="备注内容"
        )

        # 查看角色, 取得对应的ID
        lst_role(
            fetch=[reg, "role_id", f"$.rows[?(@.roleName=='{role_name}')].roleId"],
            check=[
                [f"$.rows[?(@.roleName=='{role_name}')].remark", "eq", "备注内容"],
                [f"$.rows[?(@.roleName=='{role_name}')].roleName", "eq", role_name],
                [f"$.rows[?(@.roleName=='{role_name}')].roleKey", "eq", role_name],
                [f"$.rows[?(@.roleName=='{role_name}')].roleSort", "eq", 6],
            ]
        )

    def teardown_method(self):
        reg = self.reg

        # 删除角色
        rmv_role(
            role_id=reg.role_id,
        )
        pass
