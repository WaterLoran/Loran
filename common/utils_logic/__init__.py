from .excel_assertion import ExcelAssertion
from core.mysql import *
from core.check import *
from core.fetch import *
from core.logger.logger_interface import logger

def check_excel(check):
    excel_assertion = ExcelAssertion()
    excel_assertion.do_assert(check)

def exec_mysql(sql="", host="", port="", user="", password="", db="", **kwargs):
    mysql_tool = MysqlTool()
    sql_rsp_data = mysql_tool.connect_and_exec_sql(sql=sql, host=host, port=port, user=user, password=password, db=db)
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
