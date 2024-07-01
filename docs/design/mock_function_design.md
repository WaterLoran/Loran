# Mock功能设计文档

## 为什么要使用Mock

之所以使用mock测试，是因为真实场景很难实现或者短期实现起来很困难。主要场景有：

-  真实对象可能还不存在（接口还没有完成开发）
-  真实对象很难搭建起来（[第三方支付](https://www.zhihu.com/search?q=第三方支付&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A3109319750})联调）
-  真实对象的行为很难触发（例如网络错误）
-  真实对象速度很慢（例如一个完整的数据库，在测试之前可能需要初始化）
-  真实对象可能包含不能用作测试（而不是为实际工作）的信息和方法
-  真实的对象是用户界面，或包括[用户页面](https://www.zhihu.com/search?q=用户页面&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A3109319750})在内
-  真实的对象使用了回调机制
-  真实对象的行为是不确定的（例如当前的时间或当前的温度）

## Mock服务类型

### 冷mock

生命周期贯穿于整个自动化脚本连跑期间

### 热mock

生命周期仅局限于单个脚本

### 温mock

生命周期在于多个自动化脚本期间的, 笔者不建议这么使用, 因为会给设计实现带来很大困难, 因为会使脚本逻辑不清晰, 所以要么直接转换为冷mock, 要么转换为热mock

## 设计概要

### 服务提供层

### mock的描述

1. 暴露常见的keyword, 比如url, method, body等, 并需要追加 mock_app默认信息
2. 热mock在热mock描述目录
3. 冷mock在冷mock描述目录

**对于冷mock**

存在以下两种方法, 待考虑决定

1. 冷mock使用flask来提供, 即表现为真是的web服务器, 即request请求指定接口的时候, 是请求的真实服务器, 而不是直接拦截request的请求. 各类接口使用配置文件来描述, 然后通过收集以及切面方程的方式拉起服务, 并提供统一的入口来启停mock服务. 优点:常驻研发周期,并且可多人使用.  缺点:需要有专人统一维护, 不能自行运维. 建议: 可使用第三方软件来暂时提供, 而后统一编写进去冷mock配置中.
2. 使用request_mock来提供, 即直接拦截request的请求, 并返回响应, 实现原理同样为在指定目录下描述冷mock的接口数据, 然后通过request_mock来拉起, 并提供对应的启停控制. 优点: 可以自行启停设计, 缺点:因为冷mock设计为跟随整个自动化脚本连跑的生命周期, 所以对于单个脚本的调试运行编写很不友好.

**对于热mock**

1. 使用request_mock来提供, 即直接拦截request的请求, 并返回反应, 不提供flask真实服务器的形式

### 脚本调用层

首先, 某个关键字被封装来去请求被模拟的软件, 那么这个关键字被称作 mock关键字, 本身也是一种请求方式的描述. 他有可能会去请求真实的第三方软件的接口, 也有可能会去请求 mock服务. 可通过配置来决定

参考基于描述的关键字设计方法, mock关键字,应该 暴露和正常关键字一样的参数(req_url, req_method, req_json, req_data, req_file等)

由于对被模拟软件接口的请求, 是针对于特定软件, 并且该信息不经常变, 所以, 可以将被模拟软件的信息进行一定封装并设计成配置(域名, token或者cookie的获取方法 等)

基于上述的思考, mock关键字还需追加一个参数, mock_app, 该参数将用于关联配置中的基础配置

要提供在业务脚本层使用参数去临时启停mock服务, 用于调试

### mock配置层

1. 提供全局配置来启停冷mock服务
2. 提供全局配置来启停热mock服务
3. 提供配置来切换使用真实第三方接口, 还是mock服务
4. 提供真实第三方软件的配置信息
5. 针对热mock服务提供 mock模板(即和mock关键字所用配置一致, 即mock_app默认信息)
6. mock关键字所关联的配置 和 mock服务所关联的配置 是同一份

### 参考代码


```python
import requests
import requests_mock

# 创建一个请求会话
session = requests.Session()

# 创建一个请求mock
adapter = requests_mock.Adapter()
session.mount('mock://', adapter)

# 模拟 GET 请求
adapter.register_uri('GET', 'mock://api/user/1', json={'userId': 1, 'username': 'John Doe', 'email': 'john.doe@example.com'})

# 模拟 POST 请求
def match_login_request(request):
    data = request.json()
    if data.get('username') == 'admin' and data.get('password') == 'password':
        return {'message': 'Login successful'}
    return requests_mock.create_response(request, json={'message': 'Invalid username or password'}, status_code=401)

adapter.register_uri('POST', 'mock://api/login', json=match_login_request)

# 示例函数来测试 GET 请求
def get_user(user_id):
    response = session.get(f'mock://api/user/{user_id}')
    print(response.json())

# 示例函数来测试 POST 请求
def login(username, password):
    response = session.post('mock://api/login', json={'username': username, 'password': password})
    print(response.json())

# 示例调用
get_user(1)  # 获取用户信息
login('admin', 'password')  # 登录
login('user', 'wrongpassword')  # 尝试使用错误密码登录

```

