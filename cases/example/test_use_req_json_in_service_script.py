# coding=utf8
from common.ruoyi_logic import *


class TestUseReqJsonInServcieScript:
    def setup_method(self):
        pass

    def test_use_req_json_in_service_script(self):
        reg = register({
            "user_id": None,
            "user_id2": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "hello22"
        # 此处为使用req_json, 将会和api定义中的进行融合合并, 最后再由业务脚本层的参数填充进去
        # 常用于, 后者的请求依赖前面的请求大部分相应内容 的场景, 比如表单的查询和修改
        req_json = {
            "deptId": None,  # 部门ID
            "userName": "",  # 用户名称
            "nickName": var_name,  # 用户昵称
            "password": var_name,  # 密码
            "phonenumber": "",  # 电话号码
            "email": "",
            "sex": "",  # 性别 0表示男, 1表示女
            "status": "",  # 状态, 0表示启用, 1表示停用
            "remark": "",  # 备注
            "postIds": [],  # 岗位ID
            "roleIds": []  # 角色
        }
        add_user(
            req_json=req_json,
            userName=var_name,
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
