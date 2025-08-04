from loran.logic import *


@Api.form_data
@allure.step("修改用户头像")
def mod_profile_picture(picture="猞猁.png", **kwargs):
    req_url = "/dev-api/system/user/profile/avatar"
    req_method = "POST"
    files = {"avatarfile": picture}
    data = {}
    rsp_check = {
        "msg": "操作成功",
        "code": 200
    }
    auto_fill = False
    return locals()


