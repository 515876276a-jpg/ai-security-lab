a = 0
b = 1
c = input("你想要一个多长的斐波那契数列：")
try:
    c = int(c)
except ValueError:
    print("输入的不是一个有效的整数，请重新输入。")
    exit()
if c <= 0:
    print("请输入一个正整数。")
    exit()
else:
    for i in range(c):
        print(a)
        a, b = b, a + b
