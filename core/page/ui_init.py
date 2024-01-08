class SingletonMeta(type):
    """
    功能: 以单例模式存放seleniumbase实例, 以达到全局的效果
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class RuoYiSeleniumBase(metaclass=SingletonMeta):
    def __init__(self):
        from seleniumbase import BaseCase
        self.sb: BaseCase

    def get_sb_instance(self):
        return self.sb

    def set_sb_instance(self, sb_instance):
        self.sb = sb_instance


def ui_init(sb_instance):
    epros_sb = RuoYiSeleniumBase()
    epros_sb.set_sb_instance(sb_instance)


def get_sb_instance():
    epros_sb = RuoYiSeleniumBase()
    return epros_sb.get_sb_instance()



