from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import path

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'artem_shelmin_orm'
    db_user = 'artem_shelmin_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "artem_shelmin_orm.db")

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

count = 0

@app.route("/")
@app.route("/index")
def index():
    css_path = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
        <body>
            <header>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
                <link rel="stylesheet" href="''' + css_path + '''">
            </header>
            
            <main>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                </ul>
                <ul>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                </ul>
                <ul>
                    <li><a href="/lab3">Третья лабораторная</a></li>
                </ul>
                <ul>
                    <li><a href="/lab4">Четвёртая лабораторная</a></li>
                </ul>
                <ul>
                    <li><a href="/lab5">Пятая лабораторная</a></li>
                </ul>
                <ul>
                    <li><a href="/lab6">Шестая лабораторная</a></li>
                </ul>
                <ul>
                    <li><a href="/lab7">Седьмая лабораторная</a></li>
                </ul>
                <ul>
                    <li><a href="/lab8">Восьмая лабораторная</a></li>
                </ul>
            </main>
    
            <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
        </body>
        </html>'''

logs=""
@app.errorhandler(404)
def not_found(err):
    css = url_for('static', filename='lab1/style.css')
    error_img = url_for('static', filename='lab1/404.png')
    global logs
    client_ip = request.remote_addr
    time = datetime.datetime.today()
    url = request.url
    logs += '''<div class="log-entry">[<i>''' + str(time) + '''</i>, пользователь <i>''' + client_ip + '''</i>] зашел на адрес: <i>''' + url + '''</i></div>'''
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <img src="''' + error_img + '''">
                <div>Код 404 Not Found указывает, что сервер не может найти запрашиваемый ресурс.</div>
                <div style="text-align: center;">
                    <a href="/lab1">Меню лабораторной работы 1</a>
                    <a href="/lab2">Меню лабораторной работы 2</a>
                    <a href="/lab3">Меню лабораторной работы 3</a>
                </div>
                <hr>
                <div>IP-адрес пользователя: ''' + client_ip + '''</div>
                <div>Дата доступа: ''' + str(time) + '''</div>
                <div>Лог посещений:</div>
                ''' + logs + '''
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 404

@app.errorhandler(500)
def not_found2(err):
    css_style = url_for('static', filename='lab1/style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                <div class='error1'>Внутренняя ошибка сервера! Сервер перегружен, либо произошла ошибка.</div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 500
 