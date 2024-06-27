# coding=utf8
from common.ruoyi_logic import *


class TestExecSqlWithCheckAndFetch001:
    """
    执行sql语句的例子
    """

    def setup(self):
        pass

    def test_exec_sql_with_check_and_fetch_001(self):

        reg = register({
            "a_id": None,
        })

        exec_mysql(
            sql="select role_id, role_name from sys_role;",
            host="127.0.0.1", port="3306", user="root", password="admin@123", db="ry-vue",
            check=["$.[2].role_id", "eq", 3],
            fetch=[reg, "a_id", "$.[3].role_id"]
        )

        print("a_id => ", reg.a_id)

    def teardown(self):
        pass
