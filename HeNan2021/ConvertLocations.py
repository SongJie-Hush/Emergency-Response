import pandas as pd
import requests
from requests.exceptions import ReadTimeout, ConnectTimeout
import csv

def transform(geo):
    parameters = { address : geo,  key :  ffcb321457eaf3c7a49ee5b1fc78ae2e }
    base =  https://restapi.amap.com/v3/assistant/coordinate/convert?locations=116.481499,39.990475&coordsys=gps&output=json&key=ffcb321457eaf3c7a49ee5b1fc78ae2e
    loc = 0
    try:
        response = requests.get(base, parameters, timeout=2)
        if response.status_code == 200:
            answer = response.json()
            loc = answer[ location ]
        else:
            pass
    except (ReadTimeout, ConnectTimeout):
    # ConnectTimeout指的是建立连接所用的时间，适用于网络状况正常的情况下，两端连接所用的时间。ReadTimeout指的是建立连接后从服务器读取到可用资源所用的时间。
        pass
    return loc

if __name__ == "__main__":
    loc_data = pd.read_csv("../kfc_china_stores.csv")
    raw_loc = loc_data["city"] + loc_data["address_raw"]
    with open("d:/kendeji.csv", "a", newline=  ) as csvfile:
    # a表示追加写入，w表示写入
        writer = csv.writer(csvfile)
        # 先写入columns_name
        # writer.writerow(["city", "geo_loc"])
        i = 0
        j = 0
        for item in raw_loc[j:]:
            if isinstance(raw_loc[i + j], str):
                print([item, transform(item)])
                # 表处于关闭状态才能写入或者追加写入
               writer.writerow([item, transform(item)])
            else:
                writer.writerow([raw_loc[i+j], 0])
            i = i + 1