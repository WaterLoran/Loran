from .basic import *
from easydict import EasyDict as register
from core.logic import *


@ComplexApi
@allure.step("添加用户-复合")
def add_user_complex(
        userName="", nickName="", password="",
        add_check=None, lst_check=None, restore=False, **kwargs):

    reg = register({
        "user_id": None,
    })

    # 创建用户
    add_user(
        userName=userName, nickName=nickName, password=password,
        check=add_check
    )

    # 查看用户
    lst_user(
        fetch=[
            [reg, "user_id", f"$.rows[?(@.userName=='{userName}')].userId"],
        ],
        check=lst_check
    )

    restore = {
        "rmv_user": {
            "userId": reg.user_id
        },
        "cur_restore_flag": restore
    }

    return locals()
