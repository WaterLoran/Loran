from pages import *


class TestClickableAndVisible(RuoYiUicase):

    def test_clickable_and_visible(self):
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

        # user_data_page(
        #     last_user_edit_button=[
        #         ["visible", True],
        #         ["clickable", True],
        #     ],
        # )

        user_data_page(
            last_user_edit_button=["visible", True],
            # last_user_edit_button = ["clickable", True],
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





