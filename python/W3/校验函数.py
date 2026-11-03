"""W3 公共输入校验模块。

约定：
1. 校验失败统一抛出 ValidationError，异常消息就是可以直接展示给用户的中文原因。
2. 校验通过后返回清洗过的值，例如 " 42 " 会变成 42，调用方直接使用返回值。
3. capture_error 统一捕获错误，返回 (是否成功, 结果或错误原因)，上层不必写 try。
"""

import math
import re


class ValidationError(ValueError):
    """输入校验失败，str(err) 即错误原因。"""


def _is_blank(value):
    """None 与空白字符串视为空输入。"""
    return value is None or (isinstance(value, str) and not value.strip())


def require_range(value, name="输入", minimum=None, maximum=None):
    """校验数值范围，返回原值。"""
    if minimum is not None and value < minimum:
        raise ValidationError(f"{name}不能小于 {minimum}，当前为 {value}。")
    if maximum is not None and value > maximum:
        raise ValidationError(f"{name}不能大于 {maximum}，当前为 {value}。")
    return value


def _to_int(value, name):
    """把 int、整数值的 float、数字字符串转成 int，否则抛 ValidationError。"""
    if _is_blank(value):
        raise ValidationError(f"{name}不能为空。")
    if isinstance(value, bool):
        raise ValidationError(f"{name}必须是整数，当前为布尔值 {value}。")
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValidationError(f"{name}必须是有限数值，当前为 {value}。")
        if not value.is_integer():
            raise ValidationError(f"{name}必须是整数，当前为 {value}。")
        return int(value)
    if isinstance(value, str):
        text = value.strip()
        try:
            return int(text)
        except ValueError:
            pass
        try:
            number = float(text)
        except ValueError:
            raise ValidationError(f"{name}不是有效的整数：{text}") from None
        if not math.isfinite(number) or not number.is_integer():
            raise ValidationError(f"{name}不是有效的整数：{text}") from None
        return int(number)
    raise ValidationError(f"{name}的类型不支持：{type(value).__name__}，请传入整数。")


def _to_float(value, name):
    """把 int、float、数字字符串转成 float，否则抛 ValidationError。"""
    if _is_blank(value):
        raise ValidationError(f"{name}不能为空。")
    if isinstance(value, bool):
        raise ValidationError(f"{name}必须是数字，当前为布尔值 {value}。")
    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        text = value.strip()
        try:
            number = float(text)
        except ValueError:
            raise ValidationError(f"{name}不是有效的数字：{text}") from None
    else:
        raise ValidationError(f"{name}的类型不支持：{type(value).__name__}，请传入数字。")
    if not math.isfinite(number):
        raise ValidationError(f"{name}必须是有限数值，当前为 {value}。")
    return number


def require_int(value, name="输入", minimum=None, maximum=None):
    """校验整数，支持 "12"、12.0 这类写法，并校验范围。"""
    return require_range(_to_int(value, name), name, minimum, maximum)


def require_float(value, name="输入", minimum=None, maximum=None):
    """校验数字，支持 int、float、数字字符串，并校验范围。"""
    return require_range(_to_float(value, name), name, minimum, maximum)


def require_positive_int(value, name="输入", maximum=None):
    """校验正整数。"""
    return require_int(value, name, minimum=1, maximum=maximum)


def require_non_zero(value, name="除数"):
    """校验除数不为 0。"""
    number = require_float(value, name)
    if number == 0:
        raise ValidationError(f"{name}不能为 0。")
    return number


def require_text(value, name="输入", allow_empty=False):
    """校验文本，默认不允许空串或全空白。"""
    if not isinstance(value, str):
        raise ValidationError(f"{name}必须是文本，当前为 {type(value).__name__}。")
    if not allow_empty and not value.strip():
        raise ValidationError(f"{name}不能为空。")
    return value


def require_choice(value, choices, name="选项"):
    """校验取值必须在候选集合内，返回命中的键。"""
    if _is_blank(value):
        raise ValidationError(f"{name}不能为空。")
    key = value.strip() if isinstance(value, str) else value
    if key not in choices:
        options = "、".join(str(item) for item in choices)
        raise ValidationError(f"{name}无效：{value!r}，可选值为 {options}。")
    return key


def require_number_list(values, name="输入", cast=require_float, separator=None):
    """校验一组数字。

    values 可以是 "1 2 3"、"1,2,3" 这样的字符串，也可以是列表、元组或集合。
    separator 为 None 时按英文逗号、中文逗号、空白混合拆分。
    """
    if isinstance(values, str):
        if separator is None:
            items = [item for item in re.split(r"[,，\s]+", values.strip()) if item]
        else:
            items = [item.strip() for item in values.split(separator) if item.strip()]
    elif hasattr(values, "__iter__"):
        items = list(values)
    else:
        raise ValidationError(f"{name}必须是字符串或数字序列，当前为 {type(values).__name__}。")
    if not items:
        raise ValidationError(f"{name}不能为空，至少需要一个数字。")
    result = []
    for index, item in enumerate(items, start=1):
        try:
            result.append(cast(item, f"{name}第 {index} 项"))
        except ValidationError:
            raise
        except (TypeError, ValueError) as err:
            raise ValidationError(f"{name}第 {index} 项无效：{item}（{err}）") from None
    return result


def require_int_list(values, name="输入", separator=None):
    """校验一组整数。"""
    return require_number_list(values, name, cast=require_int, separator=separator)


def require_float_list(values, name="输入", separator=None):
    """校验一组数字。"""
    return require_number_list(values, name, cast=require_float, separator=separator)


def capture_error(func, *args, **kwargs):
    """执行 func 并捕获错误，返回 (是否成功, 结果或错误原因)。"""
    try:
        return True, func(*args, **kwargs)
    except ValidationError as err:
        return False, str(err)
    except ZeroDivisionError:
        return False, "除数不能为 0。"
    except (TypeError, ValueError) as err:
        return False, f"参数有误：{err}"
