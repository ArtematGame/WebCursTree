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
                <div>
                Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории 
                так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно 
                предоставляющих лишь самые базовые возможности.
                </div>
                <a href="/">Меню лабораторных работ</a>
            </main>
    
            <footer>
                <p>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</p>
            </footer>
        </body>
        </html>'''

@app.route("/lab1/web")
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


@app.route("/lab1/400")
def code400():
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 400 Bad Request указывает, что сервер не может обработать запрос из-за неверного синтаксиса.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 400

@app.route("/lab1/401")
def code401():
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 401 Unauthorized указывает, что запрос не был применён, поскольку ему не хватает действительных учётных данных для целевого ресурса.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 401

@app.route("/lab1/402")
def code402():
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 402 Payment Required указывает, что запрос не может быть обработан до тех пор, пока не будет произведена оплата.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 402

@app.route("/lab1/403")
def code403():
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 403 Forbidden указывает, что сервер понял запрос, но отказывается его авторизовать.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 403

@app.route("/lab1/404")
def code404():
    css_style = url_for('static', filename='style.css')
    img_path = url_for("static", filename="404.png")
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <img src="''' + img_path + '''">
                <div>Код 404 Not Found указывает, что сервер не может найти запрашиваемый ресурс.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 404

@app.route("/lab1/405")
def code405():
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body class=>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 405 Method Not Allowed указывает, что метод запроса известен серверу, но не поддерживается целевым ресурсом.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 405

@app.route("/lab1/418")
def code418():
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 418 I'm a teapot указывает, что сервер отказывается заваривать кофе в чайнике. Это шуточный код ошибки.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 418