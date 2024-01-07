# from core.page import Page
from selenium.webdriver.common.by import By


# @Page.base
def user_data_page(**kwargs):
    page = {
        "title": "",
        "description": "",
        "type": "page",
        "properties": {
            "user_management_button": {
                "description": "用户管理-按钮",
                "type": "button",
                "location": [By.XPATH, "//li//span[text()='用户管理']"],
                "default_action": "click",
            },
            "new_user_button": {
                "description": "新增按钮",
                "type": "button",
                "location": [By.XPATH, "//span[text()='新增']"],
                "default_action": "click",
            },
            "edit_user_button": {
                "description": "修改按钮",
                "type": "button",
                "location": [By.XPATH, "//span[text()='修改']"],
                "default_action": "click",
            },
            "rmv_user_button": {
                "description": "删除按钮",
                "type": "button",
                "location": [By.XPATH, "//span[text()='删除']"],
                "default_action": "click",
            },
            "import_user_button": {
                "description": "导入按钮",
                "type": "button",
                "location": [By.XPATH, "//span[text()='导入']"],
                "default_action": "click",
            },
            "export_user_button": {
                "description": "导出按钮",
                "type": "button",
                "location": [By.XPATH, "//span[text()='导出']"],
                "default_action": "click",
            },
            ## 某一条数据
            "user_name_button": {
                "description": "用户名称-按钮",
                "type": "button",
                "location": [By.XPATH, "//tr[.//div[contains(text(),'var_user_name')]]/td[3]"],
                "default_action": "click",
            },
            "user_nick_name_button": {
                "description": "用户昵称-按钮",
                "type": "button",
                "location": [By.XPATH, "//tr[.//div[contains(text(),'var_user_nick_name')]]/td[4]"],
                "default_action": "click",
            },
            "user_node_delete_button": {
                "description": "其中一条流程的删除按钮",
                "type": "button",
                "location": [By.XPATH, "//tr[.//div[contains(text(),'var_user_name')]]/td[last()]//button[2]"],
                "default_action": "click",
            },
        }
    }

    return locals()
