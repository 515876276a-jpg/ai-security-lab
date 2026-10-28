data = input("请输入一组数字，用空格分隔：").strip()

try:
    numbers = [float(num) for num in data.split()]
    if not numbers:
        print("没有输入有效的数字。")
        exit()
    average = sum(numbers) / len(numbers)
    print(f"这组数字的平均值是：{average}")
except ValueError:
    print("输入无效，请确保输入的都是有效的数字。")