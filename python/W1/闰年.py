year = input("请输入年份：").strip()
try:
    year = int(year)
except ValueError:
    print("输入的不是一个有效的年份，请重新输入。")
    exit()

if (year % 4 ==0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} 是闰年。")
else:
    print(f"{year} 不是闰年。")