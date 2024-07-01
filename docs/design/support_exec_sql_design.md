# 框架支持执行sql语句

## 支持在AP层执行sql语句

最完整的功能设计可以支持到下面的这些场景

before_req_sql: 请求前执行的sql语句

before_req_sql_check: 请求前执行的sql语句对应的断言

before_req_sql_fetch: 请求前执行的sql语句对应的信息提取

after_req_sql: 请求后执行的sql语句

after_req_sql_check: 请求后执行的sql语句对应的断言

after_req_sql_fetch: 请求后执行的sql语句对应的信息提取

但似乎一般没有在执行请求前去执行sql的场景, 如果有的话, 是否应该考虑直接在业务层去执行, 因为这个sql并不是和这个请求强相关的

请求后去执行sql, 可用于数据的检查, 但是一般可在业务脚本层去操作, 更加符合测试步骤的逻辑

结论: 暂不支持在AP层默认去执行sql的功能

## 支持在业务脚本层执行sql语句

设计思路: 如果在业务脚本层执行sql语句, 通常是独立于关键字调用的, 所以应该给他单独封装一个函数.

设计为支持函数式编程, 支持业务断言, 支持业务提取信息

```python
exec_sql(
	db="epros", # 可不传, 不传则使用默认的数据 XXX
	sql="", ## sql语句
	fetch=[reg, "var_a, var_b", "NAME='mike'"],  # 仅支持查出一行数据的场景提取信息, 第二个字符串里面表示两个变量, 设计为类似于python的解包, 第三个参数为追加的筛选条件(可不传)
	check=[CHECK_TYPE, "比较表达式", target] # CHECK_TYPE支持行数line_count, column_count, cell_count, respone 即断言这些数量和响应字符串. 另外在仅一行数据的场景下, 支持对某列结果值进行断言, 可写为check=["column_name", "eq", "mike"], column_name表示列名为name
)
# 并且默认期望执行是成功的
```

## 预期的使用场景

### 查某一条数据是否存在

编写很详细的SQL语句, 断言查出来的只有一条数据

编写不太详细的sql语句, 断言check=["column_name", "eq", "a_data_name"],  即同样期望查到的数据仅有1行, 但某列值为a_data_name, 这样子会比较能够凸显业务逻辑, 因为这里强调了  a_data_name, 如果混在sql语句中, 则不够明显

## 查询某个条件下有N条数据

sql 为 select * from XX_table; 然后断言check=["line_count", "eq", N], 同理可以同样设计上支持大于小于的比较方法

## 仅执行一条sql语句

有时候, 仅仅为打开某个开关, 也就执行一条sql语句, 就行, 只要断言他执行成功(这个会默认断言的, 通常都是期望执行成功). 或者他执行后返回的字符串就行, 即check=["response", "include", "success"]