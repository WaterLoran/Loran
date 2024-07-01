from core.page import Page
from selenium.webdriver.common.by import By


@Page.base
def confirm_popup_page(**kwargs):
    page = {
        "title": "",
        "description": "",
        "type": "page",
        "properties": {
            "cancel_button": {
                "description": "取消按钮",
                "type": "button",
                "location": [By.XPATH, "//button/span[text()='取消']"],
                "default_action": "click",
            },
            "confirm_button": {
                "description": "确定按钮",
                "type": "button",
                "location": [By.XPATH, "//button/span[text()='确定']"],
                "default_action": "click",
            },
        }
    }

    return locals()
