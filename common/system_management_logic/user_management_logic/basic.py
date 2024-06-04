from core.logic import Api
import allure


@Api.json
@allure.step("添加用户-add_user")
def add_user(userName="", nickName="", password=""):
    req_url = "/dev-api/system/user"
    req_method = "POST"
    req_json = {
        "deptId": None,  # 部门ID
        "userName": "",  # 用户名称
        "nickName": "",  # 用户昵称
        "password": "",  # 密码
        "phonenumber": "",  # 电话号码
        "email": "",
        "sex": "",  # 性别 0表示男, 1表示女
        "status": "",  # 状态, 0表示启用, 1表示停用
        "remark": "",  # 备注
        "postIds": [],  # 岗位ID
        "roleIds": []  # 角色
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


@Api.form_data
@allure.step("通过导入文件来增加用户")
def mod_user_by_upload(file_name="", updateSupport=0):
    req_url = "/dev-api/system/user/importData"
    req_method = "POST"
    req_params = {
        "updateSupport": updateSupport  # 0表示不覆盖, True表示覆盖
    }
    files = {"file": file_name}
    rsp_check = {
        "code": 200
    }
    return locals()


@Api.urlencoded
@allure.step("查看用户-附带restore")
def lst_user_wtih_restore(userName="", **kwargs):
    req_url = "/dev-api/system/user/list"
    req_method = "GET"
    req_params = {
        "pageNum": 1,
        "pageSize": 10
    }
    restore = {
        "rmv_user": {
            "userId": f"$.rows[?(@.userName=='{userName}')].userId"
        }
    }
    auto_fill = False
    return locals()
