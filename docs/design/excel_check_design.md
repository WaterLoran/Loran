# Excel断言功能设计文档



## Excel数据对象

| 人员名称 | 人员账号 | 功能角色   | 业务范围  |
| -------- | -------- | ---------- | --------- |
| 张三     | 001      | 销售工程师 | 业务范围A |
| 李四     | 002      | 研发工程师 | 业务范围B |



## 业务层设计

```python
excel_check = {
    "file": "所下载的文件.xlsx",
    "condition": [
        {
            "column_name": "人员名称",  # column_index暂不支持
            "column_value": "张三"  # 支持传入列表, 即支持多个数值
        },
        {
            "column_name": "人员账号",
            "column_value": "001"
        },
    ],
    "assert_type": "equal",  # 提供集合类型的比较关系, 等于, 不等于, 包含, 不包含, 属于, 不属于
    "target": [
        {
            "column_name": "功能角色",
            "column_value": "销售工程师"  # # 支持传入列表, 即支持多个数值
        },
        {
            "column_name": "业务范围",
            "column_value": "业务范围A"
        },
    ]
}

```

## 描述说明

file: 表示将要读取这个文件来做断言

condition: 表示使用这些条件来过滤出行ID, condition对应的值是一个字典列表, 分别记录列名和列值, 列值支持传入一个列表, 列表表示在列表中的值都是可选的可用于去过滤的

target: 表示使用这些条件来过滤出行ID, target对应的值是一个字典列表, 分别记录列名和列值, 列值支持传入一个列表, 列表表示在列表中的值都是可选的可用于去过滤的

assert_type: 表示前后过滤出的行ID的比较方式, 支持等于, 不等于, 包含, 不包含, 属于, 不属于这些集合关系, 对应的英文是 equal, not_equal, contain, not_contain, in, not_in