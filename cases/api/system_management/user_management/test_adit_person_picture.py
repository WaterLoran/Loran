from common.ruoyi_logic import *


class TestPersonPicture01:
    def setup_class(self):
        pass

    def test_person_picture_01(self):
        reg = register({
            "user_id": None,
            "user_id2": None,
        })
        self.reg = reg

        mod_profile_picture(
        )


    def teardown_class(self):

        pass
