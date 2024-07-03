from loran.logic.base_api import BaseApi
import allure



@allure.step("切换用户")
def switch_to_user(user="admin"):
    api = BaseApi()
    api.update_token(user=user)

