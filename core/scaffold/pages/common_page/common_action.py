from core.page.ui_init import *
from config import *


def login_ruoyi(**kwargs):
    base_url = config.env.main.domain
    username = config.env.main.username
    password = config.env.main.password

    login_page_url = base_url + "/login?redirect=/index"
    sb = get_sb_instance()
    from seleniumbase import BaseCase
    sb: BaseCase

    sb.open(url=login_page_url)
    sb.type("//input[@placeholder='账号']", username)
    sb.type("//input[@placeholder='密码']", password)
    sb.type("//input[@placeholder='验证码']", "888\n")
    sb.maximize_window()

