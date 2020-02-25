import requests
# import json
import pymysql
# import cryptography
# import sqlalchemy
# from sqlalchemy import create_engine
import time
import datetime
import traceback

currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


conn = pymysql.connect(
    host="database-softwareengieeringproject.cuvpbui26dwd.eu-west-1.rds.amazonaws.com",  # mysql服务器地址
    port=3306,  # 端口号
    user="group20",  # 用户名
    passwd="comp30830",  # 密码
    db="segroupproject",  # 数据库名称
    charset='utf8',  # 连接编码，根据需要填写
)
cur = conn.cursor()  # 创建并返回游标
# cur.execute("DROP TABLE IF EXISTS weather")
# create a empty table
sql_table = "CREATE TABLE IF NOT EXISTS `weather` (current VARCHAR(100), lon VARCHAR(100),lat VARCHAR(100),weather_id VARCHAR(100),main VARCHAR(100),description VARCHAR(100),icon VARCHAR(100),base VARCHAR(100),temp VARCHAR(100),feels_like VARCHAR(100),temp_min VARCHAR(100),temp_max VARCHAR(100),pressure VARCHAR(100),humidity VARCHAR(100),visibility VARCHAR(100),speed VARCHAR(100),deg VARCHAR(100),gust VARCHAR(100),clouds_all VARCHAR(100),dt VARCHAR(100),sys_type VARCHAR(100),sys_id VARCHAR(100),sys_country VARCHAR(100),sunrise VARCHAR(100),sunset VARCHAR(100),timezone VARCHAR(100),id VARCHAR(100),name VARCHAR(100),cod VARCHAR(100));"
cur.execute(sql_table)


def insertWeatherIntoDB():
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q=dublin,IE&units=metric&appid=ef2f7a40c765b06a8ab8b9c674fe8808'
    weather_json = requests.get(weather_url).json()
    l = len(weather_json)

    information = []
    info_1 = []
    # info_2 = []
    info = []
    coordination = []
    # information = [str(weather_json['coord']),str(weather_json['name']),str(weather_json['banking']),str(weather_json['bike_stands'])]

    coordination = weather_json['coord']
    weather = weather_json['weather'][0]
    main = weather_json['main']
    wind = weather_json['wind']
    clouds = weather_json['clouds']
    sys = weather_json['sys']
    t = (str(coordination['lon']), str(coordination['lat']))

    w = (str(weather['id']), str(weather['main']), str(weather['description']), str(weather['icon']),
         str(weather_json['base']))
    m = (
    str(main['temp']), str(main['feels_like']), str(main['temp_min']), str(main['temp_max']), str(main['pressure']),
    str(main['humidity']))

    c = (str(clouds['all']), str(weather_json['dt']))
    s = (str(sys['type']), str(sys['id']), str(sys['country']), str(sys['sunrise']), str(sys['sunset']))
    tz = str(weather_json['timezone'])
    id = str(weather_json['id'])
    name = str(weather_json['name'])
    cod = str(weather_json['cod'])
    info_1 = (tz, id, name, cod)
    try:
        # Gust is available sometimes so we add gust with try and except block if it exists
        w2 = (str(weather_json['visibility']), str(wind['speed']), str(wind['deg']), str(wind['gust']))
        info = t + w + m + w2 + c + s + info_1
        sql_insert = "insert into weather (current, lon,lat,weather_id,main,description,icon,base,temp,feels_like,temp_min,temp_max,pressure,humidity,visibility,speed,deg,gust,clouds_all,dt,sys_type,sys_id,sys_country,sunrise,sunset ,timezone,id,name,cod) values  (" + "'" + \
                     currentTime + "'" + "," + "'" +  info[0] + "'" + "," + "'" + info[1] + "'" + "," + "'" + info[2] + "'" + "," + "'" + info[
                         3] + "'" + "," + "'" + info[4] + "'" + "," + "'" + info[5] + "'" + "," + "'" + info[
                         6] + "'" + "," + "'" + info[7] + "'" + "," + "'" + info[8] + "'" + "," + "'" + info[
                         9] + "'" + "," + "'" + info[10] + "'" + "," + "'" + info[11] + "'" + "," + "'" + info[
                         12] + "'" + "," + "'" + info[13] + "'" + "," + "'" + info[14] + "'" + "," + "'" + info[
                         15] + "'" + "," + "'" + info[16] + "'" + "," + "'" + info[17] + "'" + "," + "'" + info[
                         18] + "'" + "," + "'" + info[19] + "'" + "," + "'" + info[20] + "'" + "," + "'" + info[
                         21] + "'" + "," + "'" + info[22] + "'" + "," + "'" + info[23] + "'" + "," + "'" + info[
                         24] + "'" + "," + "'" + info[25] + "'" + "," + "'" + info[26] + "'" + "," + "'" + info[
                         27] + "'" + ");"
    except:
        w2 = (str(weather_json['visibility']), str(wind['speed']), str(wind['deg']))
        info = t + w + m + w2 + c + s + info_1
        sql_insert = "insert into weather (current, lon,lat,weather_id,main,description,icon,base,temp,feels_like,temp_min,temp_max,pressure,humidity,visibility,speed,deg,clouds_all,dt,sys_type,sys_id,sys_country,sunrise,sunset ,timezone,id,name,cod) values  (" + "'" + \
                     currentTime + "'" + "," + "'" +  info[0] + "'" + "," + "'" + info[1] + "'" + "," + "'" + info[2] + "'" + "," + "'" + info[
                         3] + "'" + "," + "'" + info[4] + "'" + "," + "'" + info[5] + "'" + "," + "'" + info[
                         6] + "'" + "," + "'" + info[7] + "'" + "," + "'" + info[8] + "'" + "," + "'" + info[
                         9] + "'" + "," + "'" + info[10] + "'" + "," + "'" + info[11] + "'" + "," + "'" + info[
                         12] + "'" + "," + "'" + info[13] + "'" + "," + "'" + info[14] + "'" + "," + "'" + info[
                         15] + "'" + "," + "'" + info[16] + "'" + "," + "'" + info[17] + "'" + "," + "'" + info[
                         18] + "'" + "," + "'" + info[19] + "'" + "," + "'" + info[20] + "'" + "," + "'" + info[
                         21] + "'" + "," + "'" + info[22] + "'" + "," + "'" + info[23] + "'" + "," + "'" + info[
                         24] + "'" + "," + "'" + info[25] + "'" + "," + "'" + info[26] + "'" + ");"

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
        insertWeatherIntoDB()
        # wait for 5 minutes
        time.sleep(30*60)


    except:
        # print error messages with traceback if error occurs
        print(traceback.format_exc())