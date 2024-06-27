import pymysql
from core.logger.logger_interface import logger

from core.check import *


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

    def update_mysql_connect_info_with_config(self, host="", port="", user="", password="", db=""):
        """
        传入的那一个字段为空字符串, 那么就从配置中读取该配置的信息
        """
        # 如果传入的port为str, 则转换为int
        if isinstance(port, str):
            port = int(port)
        return host, port, user, password, db

    def connect_and_exec_sql(self, sql="", host="", port="", user="", password="", db=""):
        host, port, user, password, db = updated_info = \
            self.update_mysql_connect_info_with_config(host=host, port=port, user=user, password=password, db=db)
        connection = self.connect_to_mysql(host=host, port=port, user=user, password=password, db=db)  # 连接数据库
        exec_res = self.exec_sql(connection, sql)  # 执行sql语句
        # 如果不是select语句的话, 则另外处理, TODO
        return exec_res


__all__ = [
    "MysqlTool",
]