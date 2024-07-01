from core.page import Page
from selenium.webdriver.common.by import By


@Page.base
def main_page(**kwargs):
    page = {
        "title": "",
        "description": "",
        "type": "page",
        "properties": {
            "home_page": {
                "description": "首页",
                "type": "button",
                "location": [By.XPATH, "//span[contains(text(),'首页')]"],
                "default_action": "click",
            },
            "system_management": {
                "description": "系统管理",
                "type": "button",
                "location": [By.XPATH, "//span[contains(text(),'系统管理')]"],
                "default_action": "click",
            },
            "system_monitor": {
                "description": "系统监控",
                "type": "button",
                "location": [By.XPATH, "//span[contains(text(),'系统监控')]"],
                "default_action": "click",
            },
            "system_tool": {
                "description": "系统工具",
                "type": "button",
                "location": [By.XPATH, "//span[contains(text(),'系统工具')]"],
                "default_action": "click",
            },
            "ruoyi_official_website": {
                "description": "若依官网",
                "type": "button",
                "location": [By.XPATH, "//span[contains(text(),'若依官网')]"],
                "default_action": "click",
            },
        }
    }

    return locals()
