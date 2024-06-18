from core.logger.logger_interface import logger
from core.context import ServiceContext

class ComplexApi:
    def __init__(self, func):
        self.func = func

    def __call__(self, **kwargs):
        # 提取出 restore 信息
        # 取出 check相关信息

        # kwargs 即为 入参键值对
        complex_fetch = self.get_service_fetch(**kwargs)

        exec_res_kwargs = self.func(**kwargs)  # 必然是先执行了部分函数之后才能, 返回restore表达式
        if "restore" in exec_res_kwargs:
            complex_restore = exec_res_kwargs["restore"]
            self.push_restore_to_context(complex_restore)

        if complex_fetch:  # 如果在业务脚本层传入了 fetch 信息
            if "reg" not in exec_res_kwargs:
                logger.error("业务脚本层传入了fetch, 但复合关键字中却没有定义register, 即没有数据源用于提取信息")
                raise
            complex_reg = exec_res_kwargs["reg"]
            self.do_complex_service_fetch(complex_reg, fetch=complex_fetch)

    def get_service_fetch(self, **kwargs):
        if "fetch" in kwargs:
            complex_fetch = kwargs["fetch"]
            return complex_fetch
        return None

    def fetch_variable_for_sphere_logic(self, reg, **kwargs):
        if "fetch" in kwargs.keys():
            fetch_info = kwargs["fetch"]
            change_two_dimensional_flag = False
            for element in fetch_info:
                if not isinstance(element, list):
                    change_two_dimensional_flag = True
                    break
            if change_two_dimensional_flag:
                fetch_info = [fetch_info]

            for fetch in fetch_info:
                var = fetch[0]
                var_name = fetch[1]
                reg_name = fetch[2]
                var[var_name] = reg[reg_name]

    def do_complex_service_fetch(self, register, fetch=None):
        self.fetch_variable_for_sphere_logic(register, fetch=fetch)

    def push_restore_to_context(self, complex_restore):
        service_context = ServiceContext()
        service_context.restore_list.append(complex_restore)



