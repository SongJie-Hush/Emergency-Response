import os
import sys
import traceback
# import pymysql
import urllib3
import requests
from bs4 import BeautifulSoup as BS

# 引入上一级目录
import os
import sys
# 使用以下代码替换：sys.path.append("../")
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append("../")
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

import pandas as pd
from pandas import DataFrame

key = "ee5e03174666669f95da30607af5f629"

# 在线验证地址：https://lbs.amap.com/tools/picker

# 高德地址逆解析
def getGEOAddress(x,y):
    add=[]
    location = str(x) + ',' + str(y)
    parameters = {'location': location, 'key': key}
    base = 'http://restapi.amap.com/v3/geocode/regeo'
    response = requests.get(base, parameters, verify=False)
    answer = response.json()
    return answer

# 高德地图地址解析获取经纬度
def getGEOCode(address):
    parameters = {'key': key, 'address': address}
    base = 'https://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters, verify=False)
    answer = response.json()
    return answer


# 程序主方法入口
if __name__ == '__main__':

    # 显示系统路径
    # print(sys.path)
    # 显示当前工作目录
    # print(os.getcwd())

    file_name = '0430'
    address_line = 3
    district_line = 2

    data_file = r"C:\Users\40576\Desktop\open" + file_name + ".xlsx"
    print(os.path.exists(data_file))

    data = pd.read_excel(data_file, sheet_name=0)
    data_ori = data
    data["解析位置"] = ""
    data["解析区域"] = ""
    data["解析坐标"] = ""
    districtCode = {"市辖区": 310100, "黄浦区": 310101, "卢湾区": 310103, "徐汇区": 310104, "长宁区": 310105,
                    "静安区": 310106, "普陀区": 310107, "闸北区": 310108, "虹口区": 310109, "杨浦区": 310110,
                    "闵行区": 310112, "宝山区": 310113, "嘉定区": 310114, "浦东新区": 310115, "金山区": 310116,
                    "松江区": 310117, "青浦区": 310118, "南汇区": 310119, "奉贤区": 310120, "崇明县": 310151}
    datashape = data.shape
    for i in range(0, datashape[0]):
        data.iat[i, district_line] = districtCode[data.iat[i, district_line]]

    address_list = []
    addressCity_list = []
    addressLocation_list = []

    for row in data.values:
        # print(row)
        address = str(row[address_line])
        # print(address)
        try:
            geo_result = getGEOCode(address)
            if geo_result is not None:
                print("逆向地理位置 [ %s ] 成功，开始解析地址..." % address)
                print(geo_result)
                status = geo_result["status"]
                info = geo_result["info"]
                infocode = geo_result["infocode"]
                count = int(geo_result["count"])
                geocodes = geo_result["geocodes"]
                if count >= 1:
                    for geocode in geocodes:
                        formatted_address = geocode["formatted_address"]
                        country = geocode["country"]
                        province = geocode["province"]
                        citycode = geocode["citycode"]
                        city = geocode["city"]
                        district = geocode["district"]
                        adcode = geocode["adcode"]
                        location = geocode["location"]
                        level = geocode["level"]

                        result_address = formatted_address
                        result_addressCity = adcode
                        result_addressLocation = location

                        print("%s - %s - %s" % (result_address,result_addressCity,result_addressLocation))

                        print("逆向地理位置 [ %s ] 解析完成！" % address)
                else:
                    print("逆向地理位置 [ %s ] 返回0个地址信息！" % address)
            else:
                print("逆向地理位置 [ %s ] 返回空！" % address)
        except Exception as location_exce:
            print("逆向地理位置 [ %s ] 异常！" % address)
            print(repr(location_exce))
            print(traceback.print_exc())

        address_list.append(result_address)
        addressCity_list.append(result_addressCity)
        addressLocation_list.append(result_addressLocation)

    # 新增列
    data['解析位置'] = address_list
    data['解析区域'] = addressCity_list
    data['解析坐标'] = addressLocation_list

    data["lat"] = ""
    data["check"] = ""
    datashape = data.shape
    for i in range(0, datashape[0]):
        strList = data.iat[i, datashape[1]-3].split(',')
        data.iat[i, datashape[1]-3] = strList[0]
        data.iat[i, datashape[1]-2] = strList[1]
        if int(data.iat[i, datashape[1]-4]) != int(data.iat[i, district_line]):
            data.iat[i, datashape[1]-1] = "疑似错误，请核查！"
    data = data.rename(columns={"解析坐标": "lon"})

    # 保存
    DataFrame(data).to_excel(r"C:\Users\40576\Desktop\open" + file_name + "_convert.xlsx", sheet_name='Sheet1', index=False, header=True)
    # with pd.ExcelWriter(data_file) as writer:
    #     data_ori.to_excel(writer, sheet_name='Sheet1')
    #     data.to_excel(writer, sheet_name='Sheet2')