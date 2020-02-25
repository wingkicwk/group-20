from flask import Flask, g, render_template, jsonify
import configparser
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
        host="database-softwareengieeringproject.cuvpbui26dwd.eu-west-1.rds.amazonaws.com",  # mysql服务器地址
        port=3306,  # 端口号
        user="group20",  # 用户名
        passwd="comp30830",  # 密码
        db="segroupproject",  # 数据库名称
        charset='utf8',  # 连接编码，根据需要填写
    )
    cur = conn.cursor()  # 创建并返回游标


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db.close()


@app.route('/')
def root():
    return render_template('index.html')
@app.route('/stations')
def get_stations():
    conn = get_db()
    # conn.row_factory = sqlite3.Row

    cur = conn.cursor()
    stations = []

    rows = cur.execute("SELECCT * from stations;")
    for row in rows:
        stations.append(dict(row))

    return jsonify(stations=stations)

if __name__ == '__main__':
    app.run(debug =True)
