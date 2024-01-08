from core.page.ui_init import *
from config import *


def login_ruoyi(**kwargs):
    base_url = config.env_ip
    username = config.env_user
    password = config.env_password

    login_page_url = base_url + "/login?redirect=/index"
    sb = get_sb_instance()
    sb.open(url=login_page_url)
    sb.type("//input[@placeholder='账号']", username)
    sb.type("//input[@placeholder='密码']", password)
    sb.type("//input[@placeholder='验证码']", "888\n")


