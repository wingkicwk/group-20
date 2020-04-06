import re
import pickle
import pandas as pd
from datetime import datetime
import pymysql
import  json
import requests
import configparser
from flask import Flask, g, render_template, jsonify
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
def connect_to_database():
    conn = pymysql.connect(
        host="group20db2.cuvpbui26dwd.eu-west-1.rds.amazonaws.com",  # mysql服务器地址
        port=3306,  # 端口号
        user="group20",  # 用户名
        passwd="comp30830",  # 密码
        db="segroupproject",  # 数据库名称
        charset='utf8',  # 连接编码，根据需要填写
    )
    return conn
connect_to_database()


def predictFutureBikes(stationNumber,unixTime):

    conn = connect_to_database()

    cur = conn.cursor()  

    NumberAndStands=[]

    cur.execute("SELECT * from Bikestation;")
    rows = cur.fetchall() 
    
    for row in rows:
        NumberAndStands.append(dict(stationNumber = int(row[0]),bike_stands = int(row[5])))

    NumberAndStandPairs={NumberAndStand['stationNumber']: NumberAndStand['bike_stands'] for NumberAndStand in NumberAndStands}

    #create datetime object from unix time
    DateToPredict = datetime.fromtimestamp(unixTime)

    main = [0,0,1,0,0,0]
    # main = 0
    feels_like=5.85

    hours = [0 for x in range(24)]
    hour = DateToPredict.hour

    hours[hour] = 1

    weekdays = [0,0,0,0,0,0,0]
    weekday = DateToPredict.weekday()
    weekdays[weekday] = 1

    # data = [feels_like,main,hour,weekday]

    data = [feels_like]+main+hours + weekdays

    # print(data)
    # df = pd.DataFrame([data], columns = [['feels_like','main','hour', 'weekday']])

    df = pd.DataFrame([data], columns = ['feels_like', 'main_Clear', 'main_Clouds', 'main_Drizzle', 'main_Fog',
       'main_Mist', 'main_Rain', 'hour_0', 'hour_1', 'hour_2', 'hour_3',
       'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10',
       'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16',
       'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22',
       'hour_23', 'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
       'weekday_4', 'weekday_5', 'weekday_6'])



        
 

    outfile = re.sub("['/()]", '', str(stationNumber))
    outfile = outfile.replace(" ","")
    #generate file path to load model

    filePath = "web/Models/" + outfile + ".pkl"


    with open(filePath, 'rb') as handle:
        multiple_linreg = pickle.load(handle)


    prediction = multiple_linreg.predict(df)
    RoundedPrediction=int(np.round(prediction))
    bikeStands=NumberAndStandPairs[stationNumber]
    
    result=bikeStands-RoundedPrediction

    return result


# predictFutureBikes(30,1586193417)