from pages import *


class TestAssertAttributeTextUI(RuoYiUicase):

    def test_assert_attribu_text_ui(self):
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
            last_user_user_name=["text", "eq", var_user_name],
            last_user_nick_name=["text", "!=", "HELLO"],
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





