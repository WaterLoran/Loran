# 恢复环境功能设计

API关键字中的关键字段描述

```python
restore = {    
    "restore_func": "rmv_term_completely",  
    "rsp_fetch": {  
        "ids": ["$.data.id", "to_list"],    
    },    
    "call_para": {  
        "ids": "ids" 
    }
}
```

## 描述说明

restore_func: 表示将会用这个key对应的值的函数去做数据恢复的操作

rsp_fetch: 表示需要从响应体中获取出来的信息, ids表示获取后所复制的对象, "$.data.id"表示用于提取数据的jsonpath表达式, to_list表示需要将获取到的数据, 转换成列表

call_para: 表示在恢复环境的时候, 调用restore_func函数, 所传入的键值对, 冒号前面的ids表示入参名称, 冒号后面的ids表示rsp_fetch中获取到的信息.

## 控制函数

将提供函数来全局打开restore功能, 即每个支持restore的关键字, 都会自动加载到后置操作中, 并去做恢复操作

支持在关键字调用的过程中,传入restore=True 参数来使单个关键字的恢复功能生效

