import requests,re
import json
import csv

url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts'
html = requests.get(url).text
unicodestr=json.loads(html)  #将string转化为dict
new_list = unicodestr.get("data")  #获取data中的内容，取出的内容为str

a = json.loads(new_list)  #对new_list再次进行load，使其变为dict才可使用


header = ['日期', '全国确诊人数', '全国疑似病例', '全国死亡人数', '全国治愈人数']
with open('./爬取结果.csv', encoding='utf-8-sig', mode='w') as f:
#编码utf-8后加-sig可解决csv中文写入乱码问题
    f_csv = csv.writer(f)
    f_csv.writerow(header)
f.close()

def save_data(data):
    with open('./爬取结果.csv', encoding='UTF-8', mode='a+', newline="") as f: # 防止自动换行
        f_csv = csv.writer(f)
        print(data)
        f_csv.writerow(data)
    f.close()

b = len(a)
i = 0
while i<b:
    data = ("\t"+a[i]['date'])  #\t解决写入csv小数（日期）自动省略前后的0问题
    confirm = (a[i]['confirm'])
    suspect = (a[i]['suspect'])
    dead = (a[i]['dead'])
    heal = (a[i]['heal'])
    i+=1
    tap = (data, confirm, suspect, dead, heal)
    save_data(tap)
print("完成爬取----")