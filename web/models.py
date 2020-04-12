
import re
import pickle

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd

from datetime import datetime, date, timedelta



def connect_to_database():
    conn = pymysql.connect(
        host="group20db2.cuvpbui26dwd.eu-west-1.rds.amazonaws.com",
        port=3306,
        user="group20",
        passwd="comp30830",
        db="segroupproject",
        charset='utf8', 
    )
    return conn


def Model(stationNumber):

    conn = connect_to_database()
    cur = conn.cursor()

    stationNumber=str(stationNumber['number'])

    df = pd.read_sql_query("SELECT * FROM segroupproject.dynamic_bikeData where number='" + stationNumber + "'", conn)
    df_2 = pd.read_sql_query("SELECT * FROM segroupproject.weather", conn)

    # Get the bike data from '2020-03-24 18:00:27'
    df = df[(pd.to_datetime(df['now_time'] ,format = '%Y-%m-%d %H:%M:%S')>= pd.to_datetime('2020-03-24 18:00:27',format = '%Y-%m-%d %H:%M:%S'))]
    df = df.reset_index(drop=True)

    df['now_time'] = pd.to_datetime(df['now_time'])

    # Get the weather data from '2020-03-24 18:01'
    df_2 = df_2[(pd.to_datetime(df_2['current'] ,format = '%Y-%m-%d %H:%M')>= pd.to_datetime('2020-03-24 18:01',format = '%Y-%m-%d %H:%M'))]
    df_2 = df_2.reset_index(drop=True)

    df_2['current'] = pd.to_datetime(df_2['current'])

    #according to the number of bike station, replicate the weather date for each line for further concat
    def copy(df,df_2):
        df_3 = pd.DataFrame()
        count = 0
        for i in range(0,len(df)-1):
            if (df_2.iloc[count,0] - df.iloc[i,5]) < pd.Timedelta('0 days 00:02:00'):
                each_row = df_2.loc[count]
                row = pd.DataFrame(each_row).T
                df_3 = df_3.append([row]*1)
                
                count +=1
        
        return df_3       
    df_3 = copy(df,df_2)

    #change the index
    df_3 = df_3.reset_index(drop=True)

    #join the two dataframe(bike and weather)
    AllBikeWeather = pd.concat([df, df_3], axis=1)

    for index, elem in AllBikeWeather['current'].items():
        if AllBikeWeather.loc[index,'timezone'] =="3600":
            
            a = elem  + timedelta(hours=1)
            
            AllBikeWeather.loc[index,'current'] = elem  + timedelta(hours=1)

    AllBikeWeather['hour'] = None
    AllBikeWeather['weekday'] = None
    for index, elem in AllBikeWeather['current'].items():

        hour = elem.hour
        weekday = elem.weekday()
        AllBikeWeather.loc[index,'hour'] = hour
        AllBikeWeather.loc[index,'weekday'] = weekday

    #drop low correlation colums
    drop_list = ['now_time','deg', 'gust','status','lon','lat' ,'base','description','icon','pressure','humidity','visibility','speed','temp_min','temp_max','clouds_all','dt','sys_type','sys_id','sys_country','sunrise','sunset','timezone','id','name','cod']
    df = AllBikeWeather.drop(columns=['now_time','deg', 'gust','status','lon','lat' ,'base','description','icon','pressure','humidity','visibility','speed','temp_min','temp_max','clouds_all','dt','sys_type','sys_id','sys_country','sunrise','sunset','timezone','id','name','cod'])

    #delete rows with null values
    def delete_null_row(df):
        lis = ['current', 'weather_id','main','temp','hour','weekday','feels_like']
        for i in lis:
            df.drop(df[df[i].isnull().values==True].index,inplace = True)
    delete_null_row(df)

    #change the data types of colums 
    df['number'] = df['number'].astype('category')
    df['available_bike_stands'] = df['available_bike_stands'].astype('int')
    df['available_bikes'] = df['available_bikes'].astype('int')
    df['last_update'] = pd.to_datetime(df['last_update'])

    df['weather_id'] = df['weather_id'].astype('category')
    df['main'] = df['main'].astype('category')
    df['temp'] = df['temp'].astype('double')
    df['feels_like'] = df['feels_like'].astype('double')

    df['weekday'] = df['weekday'].astype('category')
    df['hour'] = df['hour'].astype('category')

    # y is the target
    y = pd.DataFrame(df["available_bikes"])
    # X is everything else
    X = df.drop(["available_bikes"],1)

    # Split the dataset into two datasets: 70% training and 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=1)

    continuous_columns = X.select_dtypes(['int32','float64']).columns

    categorical_columns = df.select_dtypes(['category']).columns

    low_information_gain = ['last_update', 'current','number','weather_id','available_bike_stands','temp']

    # drop the useless column
    df_rev1 = df.copy()
    # drop low value features
    df_rev1.drop(low_information_gain, 1, inplace=True)

    # set up dummies features
    df_rev1 = pd.get_dummies(df_rev1)
    df_rev1.dtypes

    # y is the target
    y = df_rev1["available_bikes"]
    # X is everything else
    X = df_rev1.drop(["available_bikes"],1)
    # Split the dataset into two datasets: 70% training and 30% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1,  test_size=0.3)

    # need to reset the index to allow contatenation with predicted values otherwise not joining on same index...
    X_train.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    X_test.reset_index(drop=True, inplace=True)
    y_test.reset_index(drop=True, inplace=True)

    multiple_linreg = LinearRegression().fit(X_train, y_train)

    #remove special characters and create pickle file with name of stationNumbers
    outfile = re.sub("['/()]", '', stationNumber)
    outfile = outfile.replace(" ","")
    outfile = "web/Models/" + outfile + ".pkl"

    with open(outfile,'wb') as handle:
        pickle.dump(multiple_linreg,handle,pickle.HIGHEST_PROTOCOL)

def AllModels():
    """get all station numbers from database and create model for each of them"""
    conn = connect_to_database()
    cur = conn.cursor()


    stationNumberList=[] 


    getNumber = "SELECT DISTINCT number FROM segroupproject.dynamic_bikeData;"

    cur.execute(getNumber)
    rows = cur.fetchall()  

    for row in rows:
        stationNumberList.append(dict(number = int(row[0])))

    for number in stationNumberList:
        Model(number)

AllModels()