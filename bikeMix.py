# -*- coding: utf-8 -*-
import requests
import pymysql
import time 
import datetime
import traceback


conn = pymysql.connect(
    host="group20db2.cuvpbui26dwd.eu-west-1.rds.amazonaws.com",  # mysql服务器地址
    port=3306,  # 端口号
    user="group20",  # 用户名
    passwd="comp30830",  # 密码
    db="segroupproject",  # 数据库名称
    charset='utf8',  # 连接编码，根据需要填写

)

cur = conn.cursor()  # 创建并返回游标

# cur.execute("DROP TABLE IF EXISTS bikeMix")

#create a empty table
sql_table = "CREATE TABLE IF NOT EXISTS `bikeMix` (number VARCHAR(100),name VARCHAR(100), lat VARCHAR(100), lng VARCHAR(100), bike_stands VARCHAR(100),banking VARCHAR(100), available_bike_stands VARCHAR(100),available_bikes VARCHAR(100),status VARCHAR(100),last_update VARCHAR(100),now_time VARCHAR(100));"

# sql_table = "CREATE TABLE `bikeMix` (number VARCHAR(100),name VARCHAR(100), lat VARCHAR(100), lng VARCHAR(100), bike_stands VARCHAR(100),banking VARCHAR(100), available_bike_stands VARCHAR(100),available_bikes VARCHAR(100),status VARCHAR(100),last_update VARCHAR(100),now_time VARCHAR(100));"
cur.execute(sql_table)
    
def insert_bikeMixData_IntoDB():
    bike_url = 'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=a86228ee521650c4451c785d43683983f084bfa9'
    bike_json = requests.get(bike_url).json()
    l = len(bike_json)

    info_1 = []
    info_2 = []
    info = []
    # get the current time and change the format
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # print(now_time)
    for i in range(0,l):
        bike_line = bike_json[i]

        #change the unix time to format time version

        last_update = str(bike_line['last_update'])
        last_update_sub = int(last_update[:-3])
        format_time = datetime.datetime.fromtimestamp(last_update_sub).strftime('%Y-%m-%d %H:%M:%S')
        # print(format_time)


        info_1 = [str(bike_line['number']),str(bike_line['name']),str(bike_line['bike_stands']),str(bike_line['banking']),str(bike_line['available_bike_stands']),str(bike_line['available_bikes']),str(bike_line['status']),str(format_time),now_time]  #keep static data 'number' as a primary key

        position = bike_line['position']
        for j in range(0,len(position)):
            info_2 = [str(position['lat']),str(position['lng'])]
            info = info_1[:2] + info_2 + info_1[2:]


        sql_insert = "insert into bikeMix (number,name,lat,lng,bike_stands,banking,available_bike_stands,available_bikes,status,last_update,now_time) values (" + "'"+info[0]+"'" +","+ "'"+info[1]+"'" + ","+"'"+info[2]+"'" + ","+"'"+info[3]+"'" + ","+"'"+info[4]+"'" + "," + "'"+info[5]+"'"  + "," + "'"+info[6]+"'"  + "," + "'"+info[7]+"'"  + "," + "'"+info[8]+"'"  + "," + "'"+info[9]+"'"  + "," + "'"+info[10]+"'" +");"

        try:
            # 执行sql语句
            cur.execute(sql_insert)
            # 提交到数据库执行
            conn.commit()
        except:
            # Rollback in case there is any error
            conn.rollback()

while True:  
    try:
        insert_bikeMixData_IntoDB()
        # wait for 5 minutes
        time.sleep(300)
    except:
        #print error messages with traceback if error occurs
        print(traceback.format_exc())