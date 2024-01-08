from pages import *


class TestClickNavigationBar(RuoYiUicase):

    def test_click_navigation_bar(self):
        ui_init(self)

        login_ruoyi()

        main_page(
            home_page="click",
            system_management="click",
            system_monitor="click",
            system_tool="click"
        )




