#!/usr/bin/env
# -*- coding:utf-8 -*-
'''
利用高德地图api实现经纬度与地址的批量转换
'''
import requests
import pandas as pd
import time
import sys

# reload(sys)
# sys.setdefaultencoding("utf-8")

def parse():
    datas = []
    totalListData = pd.read_csv('site.csv')
    totalListDict = totalListData.to_dict('index')
    for i in range(0, len(totalListDict)):
        datas.append(str(totalListDict[i]['location']))
    return datas


def geocode(address):
    parameters = {'address': address, 'key': 'ffcb321457eaf3c7a49ee5b1fc78ae2e'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    return answer['geocode']['formatted_address']

if __name__ == '__main__':
    i = 0
    count = 0
    df = pd.DataFrame(columns=['address'])
    # locations = parse(item)
    locations = parse()
    for location in locations:
        site = geocode(location)
        df.loc[i] = site
        i = i + 1
    df.to_csv('address.csv', index=False)