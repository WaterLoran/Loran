from core.page import Page
from selenium.webdriver.common.by import By


@Page.base
def add_user_page(**kwargs):
    page = {
        "title": "若依管理系统",
        "description": "添加用户的页面, 可以通过在这个页面去编写信息, 然后提交来创建用户, 通过点击系统管理按钮, 在顶级用户管理按钮, 在点击新增用户按钮即可弹出",
        "properties": {
            "user_nick_name_input": {
                "description": "用户昵称-输入框",
                "type": "input",
                "location": [By.XPATH, "//input[@placeholder='请输入用户昵称']"],
                "default_action": "type",
            },
            "user_name_input": {
                "description": "用户名称-输入框",
                "type": "input",
                "location": [By.XPATH, "//div/div/div/div/div//input[@placeholder='请输入用户名称'][@class='el-input__inner']"],
                "default_action": "type",
            },
            "user_password_input": {
                "description": "用户密码-输入框",
                "type": "input",
                "location": [By.XPATH, "//input[@placeholder='请输入用户密码']"],
                "default_action": "type",
            },
            "ok_button": {
                "description": "确定-按钮",
                "type": "button",
                "location": [By.XPATH, "//span[text()='确 定']"],
                "default_action": "click",
            },
            "cancel_button": {
                "description": "返回-按钮",
                "type": "button",
                "location": [By.XPATH, "//span[text()='取 消']"],
                "default_action": "click",
            },
        }
    }
    return locals()

