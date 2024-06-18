from core.logic import *


@Api.json
@allure.step("添加角色-add_role")
def add_role(roleName="", roleKey="", roleSort=None, menuIds=[], remark="", **kwargs):
    req_url = "/dev-api/system/role"
    req_method = "POST"
    req_json = {
        "roleName": "",
        "roleKey": "",
        "roleSort": None,  # 排序
        "status": "0",
        "menuIds": [
            1,
            100,
            1000
        ],
        "deptIds": [],
        "menuCheckStrictly": True,
        "deptCheckStrictly": True,
        "remark": ""
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    return locals()


@Api.urlencoded
@allure.step("查看角色 lst_role")
def lst_role(**kwargs):
    req_url = "/dev-api/system/role/list"
    req_method = "GET"
    req_params = {
        "pageNum": 1,
        "pageSize": 10
    }
    rsp_check = {
        "msg": "查询成功",
        "code": 200,
    }
    return locals()


@Api.json
@allure.step("删除角色 rmv_role")
def rmv_role(role_id="", **kwargs):
    req_url = f"/dev-api/system/role/{role_id}"
    req_method = "DELETE"
    req_json = {}
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    auto_fill = False
    return locals()

