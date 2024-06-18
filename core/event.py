import time
import pytest_check
from functools import wraps
from threading import Thread
from core.logger import LoggerManager


logger = LoggerManager().get_logger("main")

class Event:
    @classmethod
    def loop(cls, times):
        """
        被该装饰器装饰的函数,将会在未抛出异常的情况下,串行循环执行times次
        如果执行过程中, 断言失败的话, 则会断言该脚本失败
        :param times: 所要执行的事情的次数
        :return:
        """
        logger.info("开始调用Event.loop,在未抛异常的情况下,将会串行循环执行目标事件{}次".format(times))

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for i in range(times):
                    func(*args, **kwargs)
                    time.sleep(1)
                logger.info("结束调用Event.loop, 已经在未抛异常的情况下,串行循环执行目标事件{}次".format(times))
            return wrapper
        return decorate

    @classmethod
    def loop_to_success(self, times):
        """
        被该装饰器装饰的函数,不论是否抛出异常, 都会尝试串行循环执行times次, 如果有成功提前返回
        :param times: 所要执行的事情的次数
        :return:
        """
        logger.info("正在调用Event.loop,在未抛异常的情况下,将会串行循环执行目标事件{}次, 直到成功, 如果指定次数还未成功这断言失败".format(times))

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                origin_num_failures = pytest_check.check_log._num_failures  # 取出执行事件前的失败次数 origin_num_failures
                step_assert_res = False

                for i in range(times):
                    logger.info(f"正在调用第{i+1}次")
                    step_assert_res = func(*args, **kwargs)
                    time.sleep(1)
                    print("loop_to_success::step_assert_res  ==> ", step_assert_res)
                    if step_assert_res:
                        break
                logger.warning(f"loop_to_success一共调用{i+1}次")

                if step_assert_res is False:
                    logger.error(f"使用loop_to_success事件来执行{i+1}次后,结果为失败")
                    assert False
                else:  # 此处loop_to_success为成功
                    logger.info(f"使用loop_to_success事件来执行{i + 1}次后,结果为成功")
                    pytest_check.check_log._num_failures = origin_num_failures  # 恢复失败次数为执行事件前的次数
                    if origin_num_failures == 0:  # 如果做这个loop_to_success之前没有错的话, 那么之前清空所有的错误, 让脚本断言成功
                        pytest_check.check_log.clear_failures()
            return wrapper
        return decorate


    @classmethod
    def force(cls, times):
        """
        被该装饰器装饰的函数,不管是否抛出异常,都串行循环执行times次
        :param times: 所要执行的事情的次数
        :return:
        """
        logger.info("正在调用Event.force,不管是否抛出异常,都会会串行循环执行目标事件{}次".format(times))

        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                origin_num_failures = pytest_check.check_log._num_failures  # 取出执行事件前的失败次数 origin_num_failures
                for i in range(times):
                    try:
                        func(*args, **kwargs)
                    except Exception as err:
                        logger.info("正在调用Event.force,抛出异常,err为{}".format(err))
                        time.sleep(1)
                pytest_check.check_log._num_failures = origin_num_failures  # 恢复失败次数为执行事件前的次数
                if origin_num_failures == 0:  # 如果做这个loop_to_success之前没有错的话, 那么之前清空所有的错误, 让脚本断言成功
                    pytest_check.check_log.clear_failures()
            return wrapper
        return decorate

    @classmethod
    def background(cls, times, delay=0.01):
        """
        被该装饰器装饰的函数将以多线程的方式执行times次,并且每两次操作之间间隔delay秒
        :param delay: 事件执行的事件间隔
        :param times: 所要执行的事情的次数
        :return:
        """
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger.info("会开启一个子进程来串行循环执行目标事件{}次".format(times))
                def bg_func():
                    for i in range(times):
                        func(*args, **kwargs)
                        time.sleep(delay)
                t = Thread(target=bg_func)
                t.start()
            return wrapper

        return decorate


if __name__ == "__main__":

    @Event.loop(5)
    def print_loop():
        print("print_loop")

    print_loop()
