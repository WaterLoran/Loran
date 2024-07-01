import pymysql
from core.context import ServiceContext


class MysqlTool:

    def connect_to_mysql(self, host="", port="", user="", password="", db=""):
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        return connection

    def exec_sql(self, connection, sql):
        with connection.cursor() as cursor:
            cursor.execute(sql)
            exec_res = cursor.fetchall()
        return exec_res

    def update_mysql_connect_info_with_config(self, host="", port="", user="", password="", db="", select=""):
        """
        传入的那一个字段为空字符串, 那么就从配置中读取该配置的信息
        """
        # 先读出config中的配置信息
        service_context = ServiceContext()
        config = service_context.config
        mysql_connect = config.database.mysql[select]

        # 取出mysql数据库中的连接信息
        host_cfg = mysql_connect["host"]
        port_cfg = mysql_connect["port"]
        user_cfg = mysql_connect["user"]
        password_cfg = mysql_connect["password"]
        db_cfg = mysql_connect["db"]

        # 如果传入的host, port, user, password, db不为空字符串, 则将这些信息对上一步的数据进行更新
        host = host_cfg if host == "" else host
        port = port_cfg if port == "" else port
        user = user_cfg if user == "" else user
        password = password_cfg if password == "" else password
        db = db_cfg if db == "" else db

        # 如果传入的port为str, 则转换为int
        if isinstance(port, str):
            port = int(port)

        return host, port, user, password, db

    def connect_and_exec_sql(self, sql="", host="", port="", user="", password="", db="", select=""):
        host, port, user, password, db = \
            self.update_mysql_connect_info_with_config(
                host=host, port=port, user=user, password=password, db=db, select=select)
        connection = self.connect_to_mysql(host=host, port=port, user=user, password=password, db=db)  # 连接数据库
        exec_res = self.exec_sql(connection, sql)  # 执行sql语句
        # 如果不是select语句的话, 则另外处理, TODO
        return exec_res


__all__ = [
    "MysqlTool",
]
