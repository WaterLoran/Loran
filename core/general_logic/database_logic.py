from core.general_logic.databases.mysql import *
from core.check import *
from core.fetch import *
from core.logger.logger_interface import logger

def exec_mysql(sql="", host="", port="", user="", password="", db="", select="main", **kwargs):
    """

    :param sql:
    :param host:
    :param port:
    :param user:
    :param password:
    :param db:
    :param select: 表示具体用那一套连接信息, main表示config目录下的database中的main这套信息
    :param kwargs:
    :return:
    """
    mysql_tool = MysqlTool()
    sql_rsp_data = mysql_tool.connect_and_exec_sql(sql=sql, host=host, port=port, user=user, password=password, db=db, select=select)
    # 提取check, 提取fetch信息
    # 如果存在check(jmespath), 则传递处理后的sql执行信息给断言功能
    if "check" in kwargs.keys():
        check = kwargs["check"]
        all_check_res = check_json_all_expect(sql_rsp_data, check)
        if all_check_res:
            logger.info(f"sql语句 => {sql} 的执行后的断言结果为  {all_check_res}")
    if "fetch" in kwargs.keys():
        fetch = kwargs["fetch"]
        fetch_json_all_value(sql_rsp_data, fetch)
    # 如果存在fetch, 则传递处理后的执行信息给提取信息功能
