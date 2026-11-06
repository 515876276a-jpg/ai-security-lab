# W3：把 W2 的 10 个脚本改写成函数。
# 每个函数只返回结果，不直接 print 或 input。
# 输入校验交给 校验函数 模块，失败时抛 ValidationError，消息即错误原因。
# 文件末尾的 demo 用 capture_error 逐条捕获，输出结果或错误原因。

import random

from 校验函数 import (
    ValidationError,
    capture_error,
    require_choice,
    require_float,
    require_int,
    require_int_list,
    require_non_zero,
    require_number_list,
    require_positive_int,
    require_text,
)

# ---------------------------------------------------------------- 1. 猜数字


def guess_num(num, data, max_num=10000):
    """单次猜测：返回偏大/偏小/猜对的提示。"""
    guess = require_int(num, "猜测的数字", minimum=1, maximum=max_num)
    target = require_int(data, "目标数字", minimum=1, maximum=max_num)
    if guess == target:
        return f"恭喜你，猜对了！答案是 {target}。"
    if guess < target:
        return "猜小了，请再试一次。"
    return "猜大了，请再试一次。"


def guess_game(max_num=10000, target=None):
    """命令行版猜数字，等价于 W2/猜数字.py 的 while 循环。"""
    limit = require_positive_int(max_num, "数字上限")
    if target is None:
        answer = random.randint(1, limit)
    else:
        answer = require_int(target, "目标数字", minimum=1, maximum=limit)
    while True:
        raw = input(f"请输入一个1到{limit}之间的整数：")
        ok, guess = capture_error(require_int, raw, "猜测的数字", 1, limit)
        if not ok:
            print(guess)
            continue
        print(guess_num(guess, answer, limit))
        if guess == answer:
            return guess


# ---------------------------------------------------------------- 2. 乘法表


def multiplication_table(size=9):
    """返回 size 行的乘法表文本。"""
    rows = require_int(size, "乘法表行数", minimum=1, maximum=99)
    lines = []
    for i in range(1, rows + 1):
        lines.append("\t".join(f"{j} * {i} = {i * j}" for j in range(1, i + 1)))
    return "\n".join(lines)


# ---------------------------------------------------------------- 3. 单位换算

UNITS = {
    "length": {"km": 1000.0, "m": 1.0, "dm": 0.1, "cm": 0.01, "mm": 0.001},
    "weight": {"t": 1000.0, "kg": 1.0, "g": 0.001, "mg": 0.000001},
}


def _unit_category(unit):
    for category, table in UNITS.items():
        if unit in table:
            return category
    return None


def _all_units():
    return "、".join(unit for table in UNITS.values() for unit in table)


def convert_unit(value, from_unit, to_unit):
    """同类别单位换算，返回换算后的数值。"""
    number = require_float(value, "数值")
    src = require_text(from_unit, "源单位").strip().lower()
    dst = require_text(to_unit, "目标单位").strip().lower()
    src_category = _unit_category(src)
    dst_category = _unit_category(dst)
    if src_category is None:
        raise ValidationError(f"未知的源单位：{src}（可用单位：{_all_units()}）。")
    if dst_category is None:
        raise ValidationError(f"未知的目标单位：{dst}（可用单位：{_all_units()}）。")
    if src_category != dst_category:
        raise ValidationError(
            f"{src}（{src_category}）与 {dst}（{dst_category}）不是同一类别，无法换算。"
        )
    table = UNITS[src_category]
    return number * table[src] / table[dst]


# ---------------------------------------------------------------- 4. 斐波那契数列


def fibonacci(count):
    """返回长度为 count 的斐波那契数列（从 0、1 开始），上限 100 项。"""
    length = require_positive_int(count, "数列长度", maximum=100)
    a, b = 0, 1
    result = []
    for _ in range(length):
        result.append(a)
        a, b = b, a + b
    return result


# ---------------------------------------------------------------- 5. 计算器

OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}

OP_ALIASES = {
    "1": "+",
    "2": "-",
    "3": "*",
    "4": "/",
    "+": "+",
    "-": "-",
    "*": "*",
    "/": "/",
}


def calculator(n1, n2, op):
    """四则运算，op 支持 + - * / 或菜单编号 1 2 3 4。"""
    left = require_float(n1, "第一个数字")
    right = require_float(n2, "第二个数字")
    symbol = OP_ALIASES[require_choice(op, OP_ALIASES, "运算符")]
    if symbol == "/":
        right = require_non_zero(right, "除数")
    return OPERATIONS[symbol](left, right)


# ---------------------------------------------------------------- 6. 列表去重


def dedupe_list(values):
    """保序去重，values 可以是 "1,2,2,3" 或 [1, 2, 2, 3]。"""
    items = require_int_list(values, "列表")
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


# ---------------------------------------------------------------- 7. 平均值


def average(numbers):
    """返回一组数字的平均值。"""
    items = require_number_list(numbers, "数字列表")
    return sum(items) / len(items)


# ---------------------------------------------------------------- 8. 闰年


def is_leap_year(year):
    """判断是否闰年。"""
    value = require_int(year, "年份", minimum=1, maximum=9999)
    return (value % 4 == 0 and value % 100 != 0) or (value % 400 == 0)


# ---------------------------------------------------------------- 9. 素数判断


def is_prime(data):
    """判断整数是否素数，负数、0、1 都返回 False。"""
    value = require_int(data, "待判断的整数")
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    factor = 3
    while factor * factor <= value:
        if value % factor == 0:
            return False
        factor += 2
    return True


def smallest_factor(data):
    """返回最小正因子（大于 1），没有则返回 None，用于说明不是素数的原因。"""
    value = require_int(data, "待判断的整数", minimum=0)
    if value < 2:
        return None
    factor = 2
    while factor * factor <= value:
        if value % factor == 0:
            return factor
        factor += 1
    return None


# ---------------------------------------------------------------- 10. 字符串反转


def reverse_text(text):
    """反转字符串。"""
    value = require_text(text, "文本")
    return value[::-1]


# ---------------------------------------------------------------- 演示入口


def _fmt(value):
    """把结果格式化成便于阅读的字符串。"""
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() else f"{value:.10g}"
    return str(value)


def _describe(title, func, args):
    ok, result = capture_error(func, *args)
    if ok:
        print(f"[成功] {title}：{_fmt(result)}")
    else:
        print(f"[失败] {title}：{result}")

if __name__ == "__main__":
    print("=== 函数实现演示 ===")
    _describe("猜数字", guess_num, (42, 50))
    _describe("乘法表", multiplication_table, (5,))
    _describe("单位换算", convert_unit, (1, "km", "m"))
    _describe("斐波那契数列", fibonacci, (10,))
    _describe("计算器", calculator, (10, 3, "/"))
    _describe("列表去重", dedupe_list, ("1,2,2,3",))
    _describe("平均值", average, ([1, 2, 3],))
    _describe("闰年判断", is_leap_year, (2020,))
    _describe("素数判断", is_prime, (29,))
    _describe("最小正因子", smallest_factor, (28,))
    _describe("字符串反转", reverse_text, ("Hello World!",))
