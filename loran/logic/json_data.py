import jsonpath
import copy
from jsonpath_ng import parse
from jsonpath_ng.jsonpath import Child, Fields, Index
from loran.logger.logger_interface import logger


class JsonData:

    class KeyError(Exception):
        def __init__(self, error_key, **kwargs):

            if len(kwargs) == 0:
                error_dict = {
                    "find_too_many_key": "The key value is incorrect. The request data contains at least two keys named $key. "
                                         "Please modify the incoming key name, that is, $parent key + $key",
                    "can_not_find_key": "The key you entered could not be found in the dictionary",
                }
            else:
                error_dict = {
                    "find_too_many_key": "The key value is incorrect. The request data contains at least two keys named $key. "
                                         "Please modify the incoming key name, that is, $parent key + $key, 关键信息为{}".format(str(kwargs["key_info"])),
                    "can_not_find_key": "The key you entered could not be found in the dictionary, 关键信息为{}".format(str(kwargs["key_info"])),
                }
            self.error_info = error_dict[error_key]

        def __str__(self):
            return repr(self.error_info)

    class FindKeyError(Exception):
        def __str__(self):
            return repr("The key you entered could not be found in the dictionary")

    data = None

    def iter_node(self, rows, road_step, target):
        if isinstance(rows, dict):
            key_value_iter = (x for x in rows.items())
        elif isinstance(rows, list):
            key_value_iter = (x for x in enumerate(rows))
        else:
            return
        for key, value in key_value_iter:
            current_path = road_step.copy()
            current_path.append(key)
            if key == target:
                yield current_path
            if isinstance(value, (dict, list)):
                yield from self.iter_node(value, current_path, target)

    def find_all_values_path_by_key(self, key: str) -> list:
        """
        传入一个key，然后对json中的所有信息进行查找，如果有匹配的key，则返回他的路径，比如[["a", "b", "c", "d"]]
        如果匹配到多个key，则返回的数据可能为[["a1", "b", "c", "d"]， ["a2", "b", "c", "d"]]
        """
        path_iter = self.iter_node(self.data, [], key)
        return list(path_iter)

    def find_all_values_path_by_jsonpath_key(self, jsonpath_key: str) -> list:
        result = jsonpath.jsonpath(self.data, jsonpath_key, result_type="IPATH")
        return result

    def get_value_of_path(self, data, path_list):
        """
        data: json格式的数据, 或者dict
        path_list: 一个路径列表, 列表中的各个元素是json_data的节点信息
        """
        alias_of_data = data
        for path in path_list:
            alias_of_data = alias_of_data[path]
        debug_str = "以上面响应日志为数据对象,根据路径列表信息{},提取的数据信息为{}".format(path_list, str(alias_of_data))
        logger.debug(debug_str)
        return alias_of_data

    def update_data(self, json_data):
        self.data = json_data

    def get_value_of_complex_key(self, data, key):
        """
        这个函数将弃用, 即将不支持这种, 复合的key去取数据的方式, 都统一为使用jsonpath的方式去获取
        """
        # 主动将数据更新到实例中，这是必须的行为
        self.update_data(data)
        if "_" not in key:
            res = self.find_all_values_path_by_key(key)  # 预期返回一个二维列表
            logger.debug("使用普通key(即不带下划线)方式查找出的值所对应的node节点路径信息列表为{}".format(res))
            if len(res) == 0:
                raise self.KeyError("can_not_find_key", key=key)
            elif len(res) > 1:
                raise self.KeyError("find_too_many_key", key_info=res)
            else:
                pass
            target_obj = self.get_value_of_path(data, res[0])
        else:
            key_list = key.split("_")

            res = self.find_all_values_path_by_key(key_list[-1])
            logger.debug("使用complex_key(即带下划线)方式查找出的值所对应的node节点路径信息列表为{}".format(res))

            # 选取出路径节点列表, 如果选不到那么就抛出一场
            # 大致场景为res = [["data", "id"], ["data", "sourceNode", "id"]], 然后传入key比如为"sourceNode_id"
            # 即key_list = ["sourceNode", "id""]
            target_path_str_list = " ".join(key_list)

            logger.debug("用户在业务脚本层传入的key的关键信息为" + target_path_str_list)

            target_obj_list = []
            for item in res:
                per_res = " ".join(item)
                if per_res.endswith(target_path_str_list):
                    target_obj_list.append(item)
            if len(target_obj_list) == 1:
                target_obj = self.get_value_of_path(data, target_obj_list[0])
            else:
                raise self.FindKeyError()

        # 提取路径节点列表, 预期res为[["a", "b", "c"]]
        return target_obj

    def edit(self, json_data: dict=None, **kwargs):
        if json_data is None:
            raise
        if "update" in kwargs.keys():
            update_content = kwargs["update"]
            json_data.update(update_content)

        if "add" in kwargs.keys():  # 和update一致
            pass
        if "mod" in kwargs.keys():  # 和update一致
            pass
        if "rmv" in kwargs.keys():  # 暂未实现
            # ["当前节点_jsonpath"]
            pass

    def edit_by_jsonpath(self, json_data=None, regex: dict=None):
        for key, value in regex.items():
            paths = jsonpath.jsonpath(json_data, key, result_type="IPATH")
            logger.debug("根据key获取到的目标所有待修改值的路径为 " + str(paths))
            if isinstance(paths, bool):
                logger.error("没有在待修改的数据中找到目标数据")
                raise
            if len(paths) > 1:
                logger.error("在待修改的数据中, 找到两个数据, 即jsonpath表达式不正确")
                raise

            paths = paths[0]  # 因为所获得的路径是二维列表, 需要转换一下

            alias_of_data = json_data
            for path in paths[0:-1]:
                if path.isdigit():
                    alias_of_data = alias_of_data[int(path)]
                else:
                    alias_of_data = alias_of_data[path]
            try:
                if paths[-1].isdigit():
                    alias_of_data[int(paths[-1])] = value
                else:
                    alias_of_data[paths[-1]] = value
            except Exception:
                logger.debug("paths[-1]" + str(paths[-1]))
                logger.debug("alias_of_data" + str(alias_of_data))

    def get_last_step(self, path):
        """
        递归获取路径的最后一步
        示例：
        - 输入：Child(Fields('a'), Fields('b')) → 返回 Fields('b')
        - 输入：Fields('m1') → 直接返回 Fields('m1')
        """
        while isinstance(path, Child):
            path = path.right
        return path

    def update_dict_by_jsonpath(self, data: dict, jsonpath_expr: str, new_value) -> dict:
        # 根据jsonpath信息, 将值更新进入数据体
        modified_data = copy.deepcopy(data)
        expr = parse(jsonpath_expr)

        matches = expr.find(modified_data)
        if not matches:
            raise ValueError(f"路径 '{jsonpath_expr}' 不存在")

        for match in matches:
            # 获取路径的最后一步
            last_step = self.get_last_step(match.path)

            # 获取父级容器
            parent = match.context.value

            # 处理不同类型
            if isinstance(last_step, Fields):
                parent[last_step.fields[0]] = new_value
            elif isinstance(last_step, Index):
                parent[last_step.index] = new_value
            else:
                raise RuntimeError(f"不支持的路径类型: {type(last_step)}")

        return modified_data

    def merge_a_dict_into_b_dict(self, a, b):
        """
        递归地将A的数据合并到B中，仅在B存在对应路径时替换。
        处理字典和列表结构，要求A和B类型一致。
        """
        if isinstance(a, dict) and isinstance(b, dict):
            # 处理字典：遍历A的键，若B中存在则合并或替换
            for key in a:
                if key in b:
                    a_val = a[key]
                    b_val = b[key]
                    # 如果都是容器类型，则递归处理
                    if isinstance(a_val, (dict)) and isinstance(b_val, (dict)):  # 仅仅对字典的数据进行递归处理, 其他的后续再补充
                        if b[key] == {}:  # 如果待填充的数据是空的, 则不用递归了, 直接替换
                            b[key] = a_val  # 直接替换
                        else:
                            self.merge_a_dict_into_b_dict(a_val, b_val)
                    else:
                        b[key] = a_val  # 否则直接替换, 可能还会有其他场景, 待补充
            return b
