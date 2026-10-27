import random

data = random.randint(1, 10000)
while True:
    guess = input("请输入一个1到10000之间的整数：").strip()
    try:
        guess = int(guess)
    except ValueError:
        print("输入的不是一个有效的整数，请重新输入。")
        continue
    if guess < 1 or guess > 10000:
        print("输入的整数不在范围内，请重新输入。")
        continue
    if guess < data:
        print("猜小了，请再试一次。")
    elif guess > data:
        print("猜大了，请再试一次。")
    else:
        print(f"恭喜你，猜对了！答案是 {data}。")
        break