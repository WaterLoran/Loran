from core.logic import Api
import allure


@Api.form_data
@allure.step("修改用户头像")
def mod_profile_picture():
    req_url = "/dev-api/system/user/profile/avatar"
    req_method = "POST"
    files = "猞猁.png"
    data = {}
    rsp_check = {
        "msg": "操作成功",
        "code": 200
    }
    return locals()


