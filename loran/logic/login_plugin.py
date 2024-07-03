import pluggy

# 定义一个Pluggy插件管理器
pm = pluggy.PluginManager("loran")

# 定义一个钩子规范
hookspec = pluggy.HookspecMarker("loran")
hookimpl = pluggy.HookimplMarker("loran")

# 定义一个钩子规范类
class MySpec:
    @hookspec
    def loran_login(self, user="admin"):
        """A hook that takes an argument and returns a string."""
        pass

    @hookspec
    def loran_update_header(self):
        """
        更新请求头的插件函数
        :return:
        """
        pass

    @hookspec
    def loran_get_authorization(self):
        """
        更新请求头的插件函数
        :return:
        """
        pass

register_flag = False

def first_register_flag():
    global register_flag
    if not register_flag:
        pm.add_hookspecs(MySpec)

        # 导入并注册插件
        from common import login

        # 注册到管理器中去
        pm.register(login.LoginPlugin())

        register_flag = True

def login_plugin_interface():
    first_register_flag()

    # 调用钩子
    pm.hook.loran_login(select="main", user="admin")


def update_headers_interface():
    first_register_flag()

    # 调用钩子
    # 这里不知道为什么, 返回的是一个字典列表, 即在字典的外围加了一个中括号, 变成了 列表
    headers_list = pm.hook.loran_update_header(select="main", user="admin")

    headers = headers_list[0]
    return headers

def get_authorization_interface():
    first_register_flag()

    # 调用钩子
    # 这里不知道为什么, 返回的是一个字典列表, 即在字典的外围加了一个中括号, 变成了 列表
    authorization = pm.hook.loran_get_authorization()
    # print("get_authorization_interface::authorization", authorization)
    # 这里会自动将他 loran_get_authorization 返回的信息, 转成列表形式, 所以, 直接返回 authorization[0] # TODO
    return authorization[0]  # 用于调试


