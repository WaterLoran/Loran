# coding=utf8
from common.ruoyi_logic import *


class TestRetryFuncExample001:
    """
    使用 retry 功能的例子
    """

    def setup_method(self):
        pass

    def test_retry_func_example_001(self):
        reg = register({
            "user_id": None,
        })
        self.reg = reg

        # 添加用户
        var_name = "retry_func_example_001"
        add_user(
            userName=var_name, nickName=var_name, password=var_name,
        )

        # 因为名字相同是不能创建成功的, 这里的脚本会去retry尝试多次, 这里需要手工在web端去删除数据, 来验证这个点, 跑完后查看日志即可
        add_user(
            userName=var_name, nickName=var_name, password=var_name,
            retry=60
        )

        lst_user_wtih_restore(
            userName=var_name,
            restore=True
        )

    def teardown_method(self):
        pass
