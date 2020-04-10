import re
import pickle
import pandas as pd
from datetime import datetime
import pymysql
import requests 
import numpy as np
import json
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

def GetRightForecast(unixTime):
    WeatherForecastURL='http://api.openweathermap.org/data/2.5/forecast?q=Dublin&appid=9ca5f328898f13bbd4559a41e958f15a'
    #get the WeatherForecast json file from api
    WeatherForecast=requests.get(WeatherForecastURL).json()

    #Returns cloest weather forecast that matched, if can't find suitable one then return false
    for i in range(len(WeatherForecast['list'])):
        if unixTime <= WeatherForecast['list'][i]['dt']:
            return WeatherForecast['list'][i]
    return False

def predictFutureBikes(stationNumber,unixTime):

    conn = connect_to_database()

    cur = conn.cursor()  

    NumberAndStands=[]

    # fetch bike stands and numbers
    cur.execute("SELECT * from Bikestation;")
    rows = cur.fetchall() 
    
    for row in rows:
        NumberAndStands.append(dict(stationNumber = int(row[0]),bike_stands = int(row[5])))

    # reformat the dictionary to make it easier to use in the following part
    NumberAndStandPairs={NumberAndStand['stationNumber']: NumberAndStand['bike_stands'] for NumberAndStand in NumberAndStands}

    FutureWeather=GetRightForecast(unixTime)

    print(FutureWeather)
    #create datetime object from unix time
    DateToPredict = datetime.fromtimestamp(unixTime)

    #list of main
    mains=['Clear','Clouds','Drizzle','Fog','Mist','Rain']

    #get main from weather forecast
    main=FutureWeather['weather'][0]['main']

    #get index of main in list mains
    index=mains.index(main)

    #flip it to 1
    mains[index] = 1

    # getting length of list 
    length = len(mains) 

    #change the list element to 0 if its not 1
    for i in range(length): 
        if mains[i]!=1:
            mains[i]=0

    #get feels_like from weather forecast
    feels_like_Kelvin=FutureWeather['main']['feels_like']

    #convert the temperature from Kelvin unit to Celsius
    feels_like= feels_like_Kelvin- 273.15 

    #create a list of 24 hours and get the hour we need from unix time then flip it to 1
    hours = [0 for x in range(24)]
    hour = DateToPredict.hour

    hours[hour] = 1

    #create a list of 7 weekdays and get the weekday we need from unix time then flip it to 1
    weekdays = [0,0,0,0,0,0,0]
    weekday = DateToPredict.weekday()
    weekdays[weekday] = 1

    data = [feels_like]+mains+hours + weekdays

    #put the data we get from given timestamp to dataframe to generate prediction
    df = pd.DataFrame([data], columns = ['feels_like', 'main_Clear', 'main_Clouds', 'main_Drizzle', 'main_Fog',
       'main_Mist', 'main_Rain', 'hour_0', 'hour_1', 'hour_2', 'hour_3',
       'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10',
       'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16',
       'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22',
       'hour_23', 'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
       'weekday_4', 'weekday_5', 'weekday_6'])

    #remove special characters and form the file name
    outfile = re.sub("['/()]", '', str(stationNumber))
    outfile = outfile.replace(" ","")
    
    #generate file path to load model
    filePath = "web/Models/" + outfile + ".pkl"

    with open(filePath, 'rb') as handle:
        multiple_linreg = pickle.load(handle)

    #predict available bikes number based on model
    prediction = multiple_linreg.predict(df)

    #round our prediction to integer
    RoundedPrediction=int(np.round(prediction))

    #get available bike stands by subtract available bikes number from total bike stands
    bikeStands=NumberAndStandPairs[stationNumber]
    AvabikeStands=bikeStands-RoundedPrediction

    result=(RoundedPrediction,AvabikeStands)

    #return a tuple including available bike and available bike stands
    return result


# predictFutureBikes(30,1586193417)