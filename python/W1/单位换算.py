
value = input("请输入一个数据：").strip()
try:
    value = float(value)
except ValueError:
    print("输入的不是一个有效的数字，请重新输入。")
    exit()

units = {
    "length": {"km": 1000, "m": 1, "dm": 0.1, "cm": 0.01, "mm": 0.001},
    "weight": {"t": 1000, "kg": 1, "g": 0.001, "mg": 0.000001}
}

src = input("请输入源单位：")
dst = input("请输入目标单位：")

from_src = src.strip().lower()
to_dst = dst.strip().lower()

for factory in units.values():
    if from_src in factory and to_dst in factory:
        converted_value = value * factory[from_src] / factory[to_dst]
        print(f"{value} {src} = {converted_value} {dst}")
        break
else:
    print("无法转换，请检查单位是否正确。")
        