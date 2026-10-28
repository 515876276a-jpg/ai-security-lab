
data = int(input("请输入一个正整数："))
if data < 0:
    print("请输入一个正整数。")
else:
    for i in range(2, data):
        if data % i == 0:
            print(f"{data}不是一个素数，它可以被{i}整除。")
            break
    else:
        print(f"{data}是一个素数")