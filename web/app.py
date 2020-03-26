from flask import Flask, g, render_template, jsonify
import configparser
import time
from datetime import datetime, date
import pandas as pd

import requests
# import json
import pymysql
import  json
config = configparser.ConfigParser()
app = Flask(__name__, static_url_path='')
# app.config.from_object('config')

def connect_to_database():
    # return engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(config.USER,
    #                                                                       config.PASSWORD,
    #                                                                       config.URI,
    #                                                                       config.PORT,
    #                                                                       config.DB),echo=True)
    conn = pymysql.connect(
        host="group20db2.cuvpbui26dwd.eu-west-1.rds.amazonaws.com",  # mysql服务器地址
        port=3306,  # 端口号
        user="group20",  # 用户名
        passwd="comp30830",  # 密码
        db="segroupproject",  # 数据库名称
        charset='utf8',  # 连接编码，根据需要填写
    )
    return conn
    # cur = conn.cursor()  # 创建并返回游标


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db.close()


@app.route('/')
def root():
    return render_template('index.html')
@app.route('/stations')
def get_stations():
    conn = connect_to_database()
    # conn = get_db()
    # # conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    stations = []

    cur.execute("SELECT * from Bikestation;")
    rows = cur.fetchall()

    for row in rows:
        stations.append(dict(number = int(row[0]), name = row[1], lat = float(row[2]), lng = float(row[3]), banking = row[4],bike_stands= row[5]))

    return jsonify(stations=stations)

@app.route('/dynamicBike')
def get_dynamicBike():
    conn = connect_to_database()

    cur = conn.cursor()
    dynamicBike = []
    sqlFetchCommand = """SELECT * from dynamic_bikeData WHERE (now_time) in (select (max(now_time))from dynamic_bikeData);;"""
    cur.execute(sqlFetchCommand)
    rows = cur.fetchall()

    for row in rows:
        dynamicBike.append(dict(number = int(row[0]), status = row[1], available_bike_stands = int(row[2]), available_bikes = int(row[3]), last_update = row[4],now_time= row[5]))

    return jsonify(dynamicBike=dynamicBike)

@app.route('/bikeMix')
def get_bikeMix():
    conn = connect_to_database()

    cur = conn.cursor()
    bikeMix = []

    sqlFetchCommand = """SELECT * from bikeMix WHERE (now_time) in (select (max(now_time))from bikeMix);;"""
    cur.execute(sqlFetchCommand)
    rows = cur.fetchall()

    for row in rows:
        bikeMix.append(dict(number = int(row[0]), name = row[1], lat = float(row[2]),lng = float(row[3]),bike_stands = int(row[4]),banking = row[5],available_bike_stands = int(row[6]), available_bikes = int(row[7]), status = row[8],last_update = row[9],now_time= row[10]))

    return jsonify(bikeMix=bikeMix)


@app.route('/weather')
def get_weather():
    conn = connect_to_database()

    cur = conn.cursor()
    weather = []
    sqlFetchCommand = """SELECT * from weather WHERE (current) in (select (max(current))from weather);;"""
    cur.execute(sqlFetchCommand)
    rows = cur.fetchall()

    for row in rows:
        weather.append(dict(main = (row[4]), description = row[5], temp = float(row[8]), feels_like = float(row[9]), temp_min =float(row[10]), temp_max =float(row[11]), pressure =int(row[12]), humidity =int(row[13]), visibility =int(row[14]), wind_speed =float(row[15]), wind_deg =row[16], gust =row[17], sunrise =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(row[23]))), sunset =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(row[24])))))

    return jsonify(weather=weather)


@app.route('/dynamic/<number_id>')
def get_available(number_id):


    conn = connect_to_database()

    cur = conn.cursor()
    bikeMix = []


    cur.execute("SELECT * from dynamic_bikeData where number=%s",(number_id))
    rows = cur.fetchall()

    for row in rows:
        last_update = row[4]
        d = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
        weekday = d.weekday()
        hour = d.hour
        bikeMix.append(dict(number = int(row[0]), available_bikes = int(row[3]), last_update = row[4],weekday = weekday,hour=hour))


    df = pd.DataFrame(bikeMix)
    means = df['available_bikes'].groupby([df['hour'], df['weekday']]).mean()
    c_df = pd.DataFrame(means)
    c_df.reset_index(inplace=True)
    for i in range(7):
        c_df[i] = None
        for index, elem in c_df['weekday'].items():

            if elem == i:
                c_df.loc[index - elem, i] = c_df.loc[index, 'available_bikes']
    specical_value = c_df[c_df['weekday'] > 0]
    c_df = c_df.drop(specical_value.index)
    c_df = c_df.drop(columns=['weekday', 'available_bikes'])
    chart_info = c_df.values.tolist()

    return jsonify(chart_info=chart_info)




if __name__ == '__main__':
    app.run(debug =True)
