import math
import random

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "被除数不能为零"
    return a / b

while True:
    print("选择运算：")
    print("1. 加法")
    print("2. 减法")
    print("3. 乘法")
    print("4. 除法")
    print("5. 退出")

    choice = input("请输入你的选择(1/2/3/4/5): ")

    if choice == '5':
        print("退出程序。")
        break
    elif choice not in ['1', '2', '3', '4']:
        print("无效的输入，请重新选择。")
        continue
    try:
        num1 = float(input("请输入第一个数字: "))
        num2 = float(input("请输入第二个数字: "))
    except ValueError:
        print("输入无效，请确保输入的是有效的数字。")
        continue

    if choice == '1':
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice == '2':
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif choice == '3':
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif choice == '4':
        result = divide(num1, num2)
        if result == "被除数不能为零":
            print(result)
        else:
            print(f"{num1} / {num2} = {result}")
    