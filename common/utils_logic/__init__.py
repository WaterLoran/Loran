from .excel_assertion import ExcelAssertion


def check_excel(check):
    excel_assertion = ExcelAssertion()
    excel_assertion.do_assert(check)
