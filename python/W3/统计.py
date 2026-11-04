import csv

with open("D:\\tya\\2020密评模拟实战考试\\test\\试卷3试题包\\数据包\\第7题\\7.2模拟测评二\\数据库\\D1-密钥表.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        