import requests
# import json
import pymysql
# import cryptography
import sqlalchemy
from sqlalchemy import create_engine


bike_url = 'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=a86228ee521650c4451c785d43683983f084bfa9'
bike_json = requests.get(bike_url).json()
l = len(bike_json)


conn = pymysql.connect(
    host="database-softwareengieeringproject.cuvpbui26dwd.eu-west-1.rds.amazonaws.com",  # mysql服务器地址
    port=3306,  # 端口号
    user="group20",  # 用户名
    passwd="comp30830",  # 密码
    db="segroupproject",  # 数据库名称
    charset='utf8',  # 连接编码，根据需要填写

)


cur = conn.cursor()  # 创建并返回游标
cur.execute("DROP TABLE IF EXISTS station")
#create a empty table
sql_table = "CREATE TABLE `Bikestation` (number  VARCHAR(100),name  VARCHAR(100),lat VARCHAR(100),lng VARCHAR(100),banking VARCHAR(100),bike_stands VARCHAR(100));"
cur.execute(sql_table)
info_1 = []
info_2 = []
info = []
position = []

for i in range(0,l):
    bike_line = bike_json[i]

    info_1 = [str(bike_line['number']),str(bike_line['name']),str(bike_line['banking']),str(bike_line['bike_stands'])]
    position = bike_line['position']
# print(position)
#     print(len(position))
    for j in range(0,len(position)):
        info_2 = [str(position['lat']),str(position['lng'])]
    info = info_1[:2] + info_2 + info_1[2:]
    # print(info)
    sql_insert = "insert into Bikestation (number,name,lat,lng,banking,bike_stands) values (" + "'"+info[0]+"'" +","+ "'"+info[1]+"'" + ","+"'"+info[2]+"'" + ","+"'"+info[3]+"'" + ","+"'"+info[4]+"'" + ","+"'"+info[5]+"'" + ");"
    # print(sql_insert)
    try:
        # 执行sql语句
        cur.execute(sql_insert)
        # 提交到数据库执行
        conn.commit()
    except:
        # Rollback in case there is any error
        conn.rollback()

    # 关闭数据库连接,没有close就可以导入？？？
# conn.close()

