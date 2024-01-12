from core.page import Page
from selenium.webdriver.common.by import By


@Page.base
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
            "last_user_user_name": {
                "description": "用户数据页面的最后一行即最后一个用户的用户名称",
                "location": [By.XPATH, "//table[@class='el-table__body']/tbody/tr[last()]/td[3]"],
            },
            "last_user_nick_name": {
                "description": "用户数据页面的最后一行即最后一个用户的用户昵称",
                "location": [By.XPATH, "//table[@class='el-table__body']/tbody/tr[last()]/td[4]"],
            },
            "last_user_edit_button": {
                "description": "用户数据页面的最后一行即最后一个用户的编辑按钮",
                "location": [By.XPATH, "//table[@class='el-table__body']/tbody/tr[last()]/td[9]/div/button[1]"],
            },
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
