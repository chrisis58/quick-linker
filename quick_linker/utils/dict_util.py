from typing import TypeVar, Callable, Dict

K = TypeVar("K")
V = TypeVar("V")

def combine_dicts(
    *dicts: Dict[K, V],
    conflict_handler: Callable[[V, V], V]
) -> Dict[K, V]:
    """
    合并传入的字典。

    :param dicts: 待合并的字典。
    :param conflict_handler: 冲突解决方法。
    :return: 合并后的字典。
    """
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key in result:
                result[key] = conflict_handler(result[key], value)
            else:
                result[key] = value
    return result
