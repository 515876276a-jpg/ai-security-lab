
damolist = input("请输入一个整数列表（用逗号分隔）：")
try:
    damolist = [int(num) for num in damolist.split(",")]
except ValueError:
    print("输入无效，请确保输入的都是有效的整数。")
    exit()
list = []
for i in damolist:
    if i not in list:
        list.append(i)
print("去重后的列表为：", list)