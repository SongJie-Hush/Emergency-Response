# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:27:51 2020
project name:2019-nCoV
@author: 帅帅de三叔
"""
import json, csv, requests  # 导入请求模块


def get_data():  # 定义获取数据并写入csv文件里的函数
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"  # 请求网址
    response = requests.get(url).json()  # 发出请求并json化处理
    # print(response) #测试一下是否获取数据了
    data = json.loads(response['data'])  # 提取数据部分
    # print(data.keys()) #获取数据组成部分['chinaTotal', 'chinaAdd', 'lastUpdateTime', 'areaTree', 'chinaDayList', 'chinaDayAddList']
    update_time = data["lastUpdateTime"]  # 更新时间

    chinaDayList = data["chinaDayList"]  # 历史数据
    with open("20200220病例.csv", "w+", newline="") as csv_file:
        writer = csv.writer(csv_file)
        header = ["date", "confirm", "suspect", "dead", "heal", "update_time"]  # 定义表头
        writer.writerow(header)
        for i in range(len(chinaDayList)):
            data_row1 = [chinaDayList[i]["date"], chinaDayList[i]["confirm"], chinaDayList[i]["suspect"],
                         chinaDayList[i]["dead"], chinaDayList[i]["heal"], update_time]
            writer.writerow(data_row1)

    chinaDayAddList = data["chinaDayAddList"]  # 历史新增数据
    with open("20200220新增病例.csv", "w+", newline="") as csv_file:
        writer = csv.writer(csv_file)
        header = ["date", "confirm", "suspect", "dead", "heal", "update_time"]  # 定义表头
        writer.writerow(header)
        for i in range(len(chinaDayAddList)):
            data_row2 = [chinaDayAddList[i]["date"], chinaDayAddList[i]["confirm"], chinaDayAddList[i]["suspect"],
                         chinaDayAddList[i]["dead"], chinaDayAddList[i]["heal"], update_time]
            writer.writerow(data_row2)

    areaTree = data["areaTree"]  # 各地方数据
    with open("20200220全国各城市病例.csv", "w+", newline="") as csv_file:
        writer = csv.writer(csv_file)
        header = ["province", "city_name", "total_confirm", "total_suspect", "total_dead", "total_heal",
                  "today_confirm", "update_time"]  # , "today_suspect", "today_dead", "today_heal"
        writer.writerow(header)
        china_data = areaTree[0]["children"]  # 中国数据
        for j in range(len(china_data)):
            province = china_data[j]["name"]  # 省份
            city_list = china_data[j]["children"]  # 该省份下面城市列表
            for k in range(len(city_list)):
                city_name = city_list[k]["name"]  # 城市名称
                total_confirm = city_list[k]["total"]["confirm"]  # 总确认病例
                total_suspect = city_list[k]["total"]["suspect"]  # 总疑似病例
                total_dead = city_list[k]["total"]["dead"]  # 总死亡病例
                total_heal = city_list[k]["total"]["heal"]  # 总治愈病例
                today_confirm = city_list[k]["today"]["confirm"]  # 今日确认病例
                # today_suspect=city_list[k]["today"]["suspect"] #今日疑似病例
                # today_dead=city_list[k]["today"]["dead"] #今日死亡病例
                # today_heal=city_list[k]["today"]["heal"] #今日治愈病例
                print(province, city_name, total_confirm, total_suspect, total_dead, total_heal, today_confirm,
                      update_time)  # today_suspect, today_dead, today_heal,
                data_row3 = [province, city_name, total_confirm, total_suspect, total_dead, total_heal, today_confirm,
                             update_time]  # , today_suspect, today_dead, today_heal
                writer.writerow(data_row3)


if __name__ == "__main__":
    get_data()
