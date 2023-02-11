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
    '''
    address = "小寨路街道长安中路33号长安大学校本部住宅区和北院宿舍区"
    location_result = getGEOCode(address)
    print("location = %s" % location_result)

    lat = 34.228959
    lng = 108.955053
    address_result = getGEOAddress(lat,lng)
    print("address = %s" % address_result)
    '''

    # 显示系统路径
    # print(sys.path)
    # 显示当前工作目录
    # print(os.getcwd())

    date = "0411"

    data_file = r"C:\Users\40576\Desktop\mapsite" + date + ".xlsx"
    # data_file = r"D:\Workspaces\PythonWorkspace\XinGuanYiQing\GEO\data\data.xlsx"
    print(os.path.exists(data_file))

    data = pd.read_excel(data_file, sheet_name=0)
    datashape = data.shape
    foodcol = [n for n in range(14, datashape[1])]
    data = pd.read_excel(data_file, sheet_name=0, skiprows=[2, 3, 4], usecols=[2, 5, 6, 7, 8, 9, 12] + foodcol)
    # df = pd.read_excel(data_file,sheet_name = "Sheet1")
    data["food"] = ""
    datashape = data.shape
    for i in range(1, datashape[0]):
        text = ""
        for j in range(7, datashape[1]-1):
            text = text + list(data.columns)[j] + "【" + data.iat[0, j] + "】：" + str(data.iat[i, j]) + "；"
        data.iat[i, datashape[1]-1] = text
        data.iat[i, 4] = data.iat[i, 3] + data.iat[i, 4]
        data.iat[i, 5] = "上海市" + data.iat[i, 3] + data.iat[i, 5]
        districtCode = {"市辖区": 310100, "黄浦区": 310101, "卢湾区": 310103, "徐汇区": 310104, "长宁区": 310105,
                        "静安区": 310106, "普陀区": 310107, "闸北区": 310108, "虹口区": 310109, "杨浦区": 310110,
                        "闵行区": 310112, "宝山区": 310113, "嘉定区": 310114, "浦东新区": 310115, "金山区": 310116,
                        "松江区": 310117, "青浦区": 310118, "南汇区": 310119, "奉贤区": 310120, "崇明县": 310230}
        data.iat[i, 3] = districtCode[data.iat[i, 3]]
    print(data.head)
    data = data.drop(data.index[0])
    data = data.drop(data.columns[[n for n in range(6, datashape[1]-1)]], axis=1)
    data = data.rename(columns={"求助编号": "helpID", "收货人": "name", "收货人电话": "phone", "行政区": "district",
                                "送货地址( 请注明所属行政区）": "location", "份数": "portion"})
    print(data.iat[0, 3])
    data["解析位置"] = ""
    data["解析区域"] = ""
    data["解析坐标"] = ""
    # areaList =  data['行政区划'].values
    # nameList =  data['社区名称'].values
    # addressList = data['送货地址'].values
    # print(addressList)


    address_list = []
    addressCity_list = []
    addressLocation_list = []

    for row in data.values:
        # print(row)
        address = str(row[5])
        print(address)
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
        if int(data.iat[i, datashape[1]-4]) != int(data.iat[i, 3]):
            data.iat[i, datashape[1]-1] = "疑似错误，请核查！"
    data = data.rename(columns={"解析坐标": "lon"})

    # 保存
    DataFrame(data).to_excel(r"C:\Users\40576\Desktop\mapsite" + date + ".xlsx", sheet_name='Sheet1', index=False, header=True)


    '''
    # 导入数据库连接
    logger.info("初始化数据库连接...")
    # 建立连接（有中文要存入数据库的话要加charset='utf8'）
    # conn = pymysql.connect(host="localhost", user="root", password="root", database="XinGuan")
    from utils import dbutil
    conn = dbutil.MySQLConnection.getConnection()
    # 创建游标
    cursor = conn.cursor()

    # 数据库查询
    logger.info("从数据库中查询 [ 社区信息 ] ...")

    table_name = "community_data"
    # SQL 查询语句(2021-12-28 15:10:00)
    sql = "SELECT id,area,name,type,level,address,result_address,result_addressCity,result_addressLocation FROM %s where result_address is null or result_address = '' order by id ; " % (table_name)
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    row_count = cursor.rowcount
    # 获取所有记录列表
    results = cursor.fetchall()
    if row_count > 0:
        logger.info("查询到已有数据 [ %d ] ，开始生成..." % row_count)
        for row in results:
            try:
                id = str(row[0])
                area =  str(row[1])
                name =  str(row[2])
                address = str(row[5])
                logger.info("%s - %s - %s - %s" % (id,area,name,address))
                geo_result = getGEOCode("%s%s" % (area,address))
                if geo_result is not None:
                    logger.info("逆向地理位置 [ %s ] 成功，开始解析地址..." % address)
                    logger.info(geo_result)
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

                            logger.info("%s - %s - %s" % (result_address,result_addressCity,result_addressLocation))

                            logger.info("逆向地理位置 [ %s ] 解析完成！" % address)

                            # 更新数据库
                            logger.info("开始更新数据库...")
                            # sql语句
                            update_sql = (
                                "update %s set result_address = '%s',result_addressCity = '%s', result_addressLocation = '%s' WHERE id = '%s' and address = '%s' " %
                                (
                                    table_name,result_address,result_addressCity,result_addressLocation,id,address
                                )
                            )
                            # 执行SQL语句
                            cursor.execute(update_sql)
                            # 提交到数据库执行
                            conn.commit()
                            logger.info("更新 [ %s - %s ] 的信息到数据库成功！" % (id, address))
                    else:
                        logger.info("逆向地理位置 [ %s ] 返回0个地址信息！" % address)
                else:
                    logger.info("逆向地理位置 [ %s ] 返回空！" % address)
            except Exception as location_exce:
                logger.info("逆向地理位置 [ %s ] 异常！" % address)
                logger.info(repr(location_exce))
                logger.info(traceback.print_exc())
    else:
        logger.info("未查询到数据！")
    '''

"""
# 导入数据库连接
    logger.info("初始化数据库连接...")
    # 建立连接（有中文要存入数据库的话要加charset='utf8'）
    # conn = pymysql.connect(host="localhost", user="root", password="root", database="XinGuan")
    from utils import dbutil
    conn = dbutil.MySQLConnection().getConnection()
    # 创建游标
    cursor = conn.cursor()

    # 数据库查询
    logger.info("从数据库中查询 [ 社区信息 ] ...")

    table_name = "risk_data"
    # SQL 查询语句(2021-12-28 15:10:00)
    sql = "SELECT cityCode,provinceName,cityName,areaName,communityName,levelCode,address,addressCity,addressLocation,latestDate,updateTime FROM %s where addressLocation is null or addressLocation = '' ; " % (table_name)
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    row_count = cursor.rowcount
    # 获取所有记录列表
    results = cursor.fetchall()
    if row_count > 0:
        logger.info("查询到已有数据 [ %d ] ，开始生成..." % row_count)
        for row in results:
            try:
                cityCode = str(row[0])
                provinceName =  str(row[1])
                cityName =  str(row[2])
                areaName =  str(row[3])
                communityName = str(row[4])

                address = str(row[6])
                addressCity = str(row[7])
                addressLocation = str(row[8])

                logger.info("%s - %s - %s - %s" % (provinceName,cityName,areaName,communityName))

                # cityCode = item["cityCode"]
                # provinceName = item["provinceName"]
                # cityName = item["cityName"]
                # areaName = item["areaName"]
                # communityName = item["communityName"]
                # levelCode = item["levelCode"]
                # latestDate = item["latestDate"]
                # updateTime = item["updateTime"]

                # 逆向地址位置
                location_result = None
                try:
                    location_result = getGEOCode("%s%s%s" % (provinceName, cityName, communityName))
                    if location_result is not None:
                        logger.info("逆向地理位置 [ %s - %s - %s ] 成功，开始解析地址..." % (provinceName, cityName, communityName))
                        logger.info(location_result)
                        status = location_result["status"]
                        info = location_result["info"]
                        infocode = location_result["infocode"]
                        count = int(location_result["count"])
                        geocodes = location_result["geocodes"]
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

                                address = formatted_address
                                addressCity = adcode
                                addressLocation = location

                                logger.info("逆向地理位置 [ %s ] 解析完成！" % communityName)
                        else:
                            logger.info("逆向地理位置 [ %s ] 返回0个地址信息！" % communityName)
                    else:
                        logger.info("逆向地理位置 [ %s ] 返回空！" % communityName)
                except Exception as location_exce:
                    logger.info("逆向地理位置 [ %s ] 异常！" % communityName)
                    logger.info(repr(location_exce))
                    logger.info(traceback.print_exc())

                # 更新数据库
                logger.info("开始更新数据库...")
                # sql语句
                update_sql = (
                    "update %s set address = '%s',addressCity = '%s', addressLocation = '%s' WHERE cityCode = '%s' and provinceName = '%s' and cityName = '%s' and areaName = '%s' and communityName = '%s' ; " %
                    (
                        table_name,address,addressCity,addressLocation,cityCode,provinceName,cityName,areaName,communityName
                    )
                )
                # 执行SQL语句
                cursor.execute(update_sql)
                # 提交到数据库执行
                conn.commit()
                logger.info("更新 [ %s - %s ] 的信息到数据库成功！" % (id, address))
            except Exception as location_exce:
                logger.info("逆向地理位置 [ %s ] 异常！" % address)
                logger.info(repr(location_exce))
                logger.info(traceback.print_exc())
    else:
        logger.info("未查询到数据！")

"""

