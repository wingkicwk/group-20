import re
import pickle
import pandas as pd
from datetime import datetime
import pymysql

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


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db.close()




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

    #fetch weather data for requested time
    futureWeatherJson = DBjson.matchWeatherForecast(unixTime)

    main = 0
    feels_like=1

    hour = DateToPredict.hour

    #extract day from datetime object
    weekday = predictionDate.weekday()

    #combine all relevant data into one list to generate dataframe 
    data = [main,feels_like,hour] + weekday

    #generate a dataframe from unixTime 
    df = pd.DataFrame([data], columns = ['main','feels_like','hour', 'weekday'])



#    Index(['feels_like', 'main_Clear', 'main_Clouds', 'main_Drizzle', 'main_Fog',
#        'main_Mist', 'main_Rain', 'hour_0', 'hour_1', 'hour_2', 'hour_3',
#        'hour_4', 'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10',
#        'hour_11', 'hour_12', 'hour_13', 'hour_14', 'hour_15', 'hour_16',
#        'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22',
#        'hour_23', 'weekday_0', 'weekday_1', 'weekday_2', 'weekday_3',
#        'weekday_4', 'weekday_5', 'weekday_6'],
#       dtype='object')   



    #remove special characters and whitespace from station name to generate file name
    outfile = re.sub("['/()]", '', stationNumber)
    outfile = outfile.replace(" ","")
    #generate file path to load model

    filePath = "Models/" + outfile + ".pkl"


    with open(filePath, 'rb') as handle:
        model = pickle.load(handle)
        
    #predict using loaded model
    prediction = model.predict(df)
    
    result = (round(prediction[0]),round((umberAndStandPairs[stationNumber])-prediction[0]))
    
    #return tuple containing available bikes and available stands
    return result