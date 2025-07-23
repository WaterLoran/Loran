# coding=utf8
from common.ruoyi_logic import *


class TestExecSqlWithCheckAndFetch001:
    """
    执行sql语句的例子
    """

    def setup_method(self):
        pass

    def test_exec_sql_with_check_and_fetch_001(self):

        reg = register({
            "a_id": None,
        })

        # 通常请狂热下是这样子使用的, 即选择表示为main的数据库配置去连接数据库, 然后执行下面的sql语句, 再去做check和fetch
        exec_mysql(
            sql="select role_id, role_name from sys_role;",
            host="127.0.0.1", port="3306", user="root", password="admin@123", db="ry-vue",
            check=["$.[2].role_id", "eq", 3],
            fetch=[reg, "a_id", "$.[3].role_id"]
        )

        # 打印提取出来的信息
        print("a_id => ", reg.a_id)

        # 不指定 mysql数据库的连接信息, 即直接使用 标识为 main的数据库, 相当于select = main
        exec_mysql(
            sql="select role_id, role_name from sys_role;",
            check=["$.[2].role_id", "eq", 3],
            select="second_db"
        )

        # 也可以指定某个数据库, 然后再去, 修改其中某个信息host
        exec_mysql(
            sql="select role_id, role_name from sys_role;",
            check=["$.[2].role_id", "eq", 3],
            select="second_db",
            host="127.0.0.1"
        )


    def teardown_method(self):
        pass
