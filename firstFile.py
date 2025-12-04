print("Dad!!")
# BMI计算 BMI = 体重 / （身高 ** 2）
# user_weight = float(input("请输入你的体重（单位：kg）："))
# user_height = float(input("请输入你的身高（单位：m）："))
#
# user_BMI = user_weight / (user_height ** 2)
#
# print("你的BMI为：" + str(user_BMI))

with open("./ft.txt", "w", encoding= "utf-8") as f:
    f.write("opten打开文件，传入值为--路径--操作--读写方法\n")
    f.write("我欲乘风归去，\n")
    f.write("又恐琼楼玉宇，\n")
    f.write("高处不胜寒。\n")

f = open("./ft.txt", "a", encoding= "utf-8")
f.write("起舞弄清影，\n")
f.write("何似在人间。")
f.close()

f = open("./ft.txt", "r", encoding="utf-8")
line = f.readline()
while line:
    print(line)
    line = f.readline()
f.close()