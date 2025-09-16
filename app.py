from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)
count = 0

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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
            </main>
    
            <footer>
                <p>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</p>
            </footer>
        </body>
        </html>'''

@app.route("/lab1")
def lab1():
    css_path = url_for("static", filename="style.css")
    return '''<!doctype html>
        <html>
        <head>
            <title>Лабораторныя 1</title>
        </head>
        <body>
            <header>
                <link rel="stylesheet" href="''' + css_path + '''">
            </header>
            
            <main>
                <p>
                Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории 
                так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно 
                предоставляющих лишь самые базовые возможности.
                </p>
                <a href="/">Меню лабораторных работ</a>
            </main>
    
            <footer>
                <p>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</p>
            </footer>
        </body>
        </html>'''

@app.route("/lab1/web")
@app.route("/")
def web():
    return '''<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Шельмин Артём Евгеньевич"
    group = "ФБИ-31"
    faculty = "ФБ"
    
    return '''<!doctype html>
        <html>
           <body>
               <p>Студент: ''' + name + '''</p>
               <p>Группа: ''' + group + '''</p>
               <p>Факультет: ''' + faculty + '''</p>
               <a href="/lab1/web">web</a>
           </body>
        </html>'''

@app.route("/lab1/image")
def image():
    img_path = url_for("static", filename="cruser.jpg")
    css_path = url_for("static", filename="lab1.css")
    
    return '''<!doctype html>
        <html>
           <head>
               <link rel="stylesheet" href="''' + css_path + '''">
           </head>
           <body>
               <h1>Land Cruiser 200</h1>
               <img src="''' + img_path + '''">
           </body>
        </html>'''

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''<!doctype html>
        <html>
            <body>
                Сколько раз вы сюда заходили: ''' + str(count) + '''
                <hr>
                Дата и время: ''' + str(time) + ''' <br>
                Запрошенный адрес: ''' + str(url) + ''' <br>
                Ваш IP-адрес: ''' + str(client_ip) + ''' <br>
                <hr>
                <a href="/lab1/counter/clear">Очистить счетчик</a>
            </body>
        </html>'''

@app.route("/lab1/counter/clear")
def clear_counter():
    global count
    count = 0
    return '''<!doctype html>
        <html>
            <body>
                <h1>Счетчик очищен!</h1>
                <p>Текущее значение счетчика: ''' + str(count) + '''</p>
                <a href="/lab1/counter">Вернуться к счетчику</a>
            </body>
        </html>'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''<!doctype html>
        <html>
            <body>
                <h1>Создано успешно</h1>
                <div><i>что-то создано...</i></div>
            </body>
        </html>''', 201