from core.logic import Api
import allure


@Api.json
@allure.step("添加用户-add_user")
def add_user(userName="", nickName="", password=""):
    req_url = "/dev-api/system/user"
    req_method = "POST"
    req_json = {
        "userName": "",  # $..userName
        "nickName": "",
        "password": "",
        "status": "0",
        "postIds": [],
        "roleIds": []
    }
    rsp_check = {
        "msg": "操作成功",
        "code": 200,
    }
    return locals()


@Api.urlencoded
@allure.step("查看用户")
def lst_user():
    req_url = "/dev-api/system/user/list"
    req_method = "GET"
    req_params = {
        "pageNum": 1,
        "pageSize": 10
    }
    return locals()


@Api.json
@allure.step("删除用户")
def rmv_user(userId=""):
    req_url = f"/dev-api/system/user/{userId}"
    req_method = "DELETE"
    req_json = {}
    auto_fill = False
    return locals()
