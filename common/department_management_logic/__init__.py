from loran.logic import *


@Api.json
@allure.step("新增部门")
def add_department(deptName="", **kwargs):
    req_url = "dev-api/system/dept"
    req_method = "POST"
    req_json = {
        "parentId": 100,  # 若依顶级部门的ID
        "deptName": "",
        "orderNum": 99,
        "status": "0"
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200
    }
    return locals()

@Api.json
@allure.step("新增部门")
def lst_department(**kwargs):
    req_url = "dev-api/system/dept/list"
    req_method = "GET"
    req_json = {}
    rsp_check = {
        "msg": "操作成功",
        "code": 200
    }
    return locals()


@Api.json
@allure.step("新增部门")
def rmv_department(departmentId=None, **kwargs):
    req_url = f"/dev-api/system/dept/{departmentId}"
    req_method = "DELETE"
    req_json = {}
    rsp_check = {
        "msg": "操作成功",
        "code": 200
    }
    auto_fill=False
    return locals()

