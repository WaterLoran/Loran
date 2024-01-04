from core.logic.base_api import BaseApi
import allure



@allure.step("切换用户")
def switch_to_user(user="admin"):
    api = BaseApi()
    api.login(user=user)

