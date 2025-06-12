from flask import Flask
from flask_mysqldb import MySQL

def iniciar_bd ():
    mysql = MySQL()
    app=Flask(__name__)
    app.config['MYSQL_HOST']='localhost'
    app.config['MYSQL_PORT'] = 3307
    app.config['MYSQL_USER']='root'
    app.config['MYSQL_PASSWORD']=''
    app.config['MYSQL_DB']='rentas_dvds' 
    app.secret_key ='mysecretkey'
    mysql.init_app(app)
    return app, mysql