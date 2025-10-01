from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1
from lab2 import lab2

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)

count = 0

@app.route("/")
@app.route("/index")
def index():
    css_path = url_for("static", filename="style.css")
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
            </main>
    
            <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
        </body>
        </html>'''

logs=""
@app.errorhandler(404)
def not_found(err):
    css = url_for('static', filename='style.css')
    error_img = url_for('static', filename='404.png')
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
                </div>
                <hr>
                <div>IP-адрес пользователя: ''' + client_ip + '''</div>
                <div>Дата доступа: ''' + str(time) + '''</div>
                <div>Лог посещений:</div>
                ''' + logs + '''
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 404

@app.errorhandler(500)
def not_found2(err):
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                <div class='error1'>Внутренняя ошибка сервера! Сервер перегружен, либо произошла ошибка.</div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 500
