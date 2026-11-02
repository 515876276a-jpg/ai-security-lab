ops = {'1':('+', lambda a,b:a+b), '2':('-', lambda a,b:a-b), '3':('*', lambda a,b:a*b), '4':('/', lambda a,b:a/b)}
while True:
    print("选择运算：\n1. 加法\n2. 减法\n3. 乘法\n4. 除法\n5. 退出")
    c = input("请输入你的选择(1/2/3/4/5): ")
    if c == '5':
        print("退出程序。")
        break
    if c not in ops:
        print("无效的输入，请重新选择。")
        continue
    try:
        n1, n2 = float(input("请输入第一个数字: ")), float(input("请输入第二个数字: "))
    except ValueError:
        print("输入无效，请确保输入的是有效的数字。")
        continue
    sym, func = ops[c]
    if c == '4' and n2 == 0:
        print("除数不能为0")
    else:
        print(f"{n1} {sym} {n2} = {func(n1, n2)}")