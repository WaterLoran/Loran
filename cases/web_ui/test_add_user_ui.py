from pages import *


class TestAddUserUi(RuoYiUicase):

    def setUp(self, masterqa_mode=False):
        super().setUp()

    def test_add_user_ui(self):
        ui_init(self)

        login_ruoyi()

        main_page(
            home_page="click",
            system_management="click",
        )

        user_data_page(
            user_management_button="click",
            new_user_button="click",
        )

        var_user_name = "loran888"
        add_user_page(
            user_nick_name_input=var_user_name,
            user_name_input=var_user_name,
            user_password_input=var_user_name,
            ok_button="click",
        )

        user_data_page(
            user_node_delete_button={
                "var_user_name": var_user_name,
                "action": "click"
            }
        )

        confirm_popup_page(
            confirm_button="click"
        )

    def teardown_method(self):
        super().tearDown()
        pass




