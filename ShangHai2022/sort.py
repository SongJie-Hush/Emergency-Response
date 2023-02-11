n = int(input())
m = int(input())
def getSum(x):
    s = 0
    t = 1
    while t != 0:
        t = x % 10    #先求个位
        s += t
        x = x//10	#除去个位，一遍下个循环再次求个位整数
        t = x
    return s
class number:  # 固定格式
    def __init__(self):  # 固定格式
        self.num = 0
        self.sum = 0

list1 = []  # 创建空列表
for i in range(1, n+1):
    list1.append(number())
    list1[i-1].num = i
    list1[i-1].sum = getSum(i)
list1.sort(key=lambda x: (x.sum, x.num))

print(list1[m-1].num)
