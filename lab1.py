from flask import Blueprint, url_for, request, redirect, abort
import datetime
lab1 = Blueprint('lab1', __name__)

count = 0

@lab1.route("/lab1/")
def lab():
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html>
            <head>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <link rel="stylesheet" href="''' + css_style + '''">
            </head>
            <body>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>
                Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории 
                так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно 
                предоставляющих лишь самые базовые возможности.
                </div>
                <div>
                    <a href="/">Меню лабораторных работ</a>
                </div>
                <h2>Список роутов:</h2>
                <div class="center-block">
                    <ol>
                        <li><a href="/">Корень сайта</a></li>
                        <li><a href="/lab1/web">Веб-сервер</a></li>
                        <li><a href="/lab1/author">Автор</a></li>
                        <li><a href="/lab1/image">Изображение</a></li>
                        <li><a href="/lab1/counter">Счетчик</a></li>
                        <li><a href="/lab1/counter/clear">Сбор счетчика</a></li>
                        <li><a href="/lab1/info">Информация</a></li>
                        <li><a href="/lab1/created">Что-то создано</a></li>
                        <li><a href="/lab1/400">Код ответа 400</a></li>
                        <li><a href="/lab1/401">Код ответа 401</a></li>
                        <li><a href="/lab1/402">Код ответа 402</a></li>
                        <li><a href="/lab1/403">Код ответа 403</a></li>
                        <li><a href="/lab1/404">Код ответа 404</a></li>
                        <li><a href="/lab1/405">Код ответа 405</a></li>
                        <li><a href="/lab1/418">Код ответа 418</a></li>
                        <li><a href="/lab1/experiment">Обработчик</a></li>
                    </ol>
                </div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>'''

@lab1.route("/lab1/web")
def web():
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
               <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
           </body>
        </html>''', 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@lab1.route("/lab1/author")
def author():
    name = "Шельмин Артём Евгеньевич"
    group = "ФБИ-31"
    faculty = "ФБ"
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <p>Студент: ''' + name + '''</p>
                <p>Группа: ''' + group + '''</p>
                <p>Факультет: ''' + faculty + '''</p>
                <a href="/lab1/web">web</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>'''

@lab1.route("/lab1/image")
def image():
    img_path = url_for("static", filename="lab1/cruser.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
    return '''<!doctype html>
        <html>
           <head>
               <link rel="stylesheet" href="''' + css_path + '''">
           </head>
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h1>Land Cruiser 200</h1>
                <img src="''' + img_path + '''">
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
           </body>
        </html>''', {
            "Content-Language": "en, ase, ru",
            "Car-Model": "Land-Cruiser-200",
            "Author": "Shelmin Artem"
            }


@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css_style + '''">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                Сколько раз вы сюда заходили: ''' + str(count) + '''
                <hr>
                Дата и время: ''' + str(time) + ''' <br>
                Запрошенный адрес: ''' + str(url) + ''' <br>
                Ваш IP-адрес: ''' + str(client_ip) + ''' <br>
                <hr>
                <a href="/lab1/counter/clear">Очистить счетчик</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>'''


@lab1.route("/lab1/counter/clear")
def clear_counter():
    global count
    count = 0
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css_style + '''">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h2>Счетчик очищен!</h2>
                <div>Текущее значение счетчика: ''' + str(count) + '''</div>
                <div>
                <a href="/lab1/counter">Вернуться к счетчику</a>
                </div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>'''


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@lab1.route("/lab1/created")
def created():
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css_style + '''">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h2>Создано успешно</h2>
                <div><i>что-то создано...</i></div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>''', 201


@lab1.route("/lab1/400")
def code400():
    css_style = url_for("static", filename="lab1/style.css")
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


@lab1.route("/lab1/401")
def code401():
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 401 Unauthorized указывает, что запрос не был применён, поскольку ему не хватает действительных учётных данных для целевого ресурса.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 401


@lab1.route("/lab1/402")
def code402():
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 402 Payment Required указывает, что запрос не может быть обработан до тех пор, пока не будет произведена оплата.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 402


@lab1.route("/lab1/403")
def code403():
    css_style = url_for("static", filename="lab1/style.css")
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>Код 403 Forbidden указывает, что сервер понял запрос, но отказывается его авторизовать.</div>
                <a href="/lab1">Меню лабораторной работы 1</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 403


@lab1.route("/lab1/405")
def code405():
    css_style = url_for("static", filename="lab1/style.css")
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


@lab1.route("/lab1/418")
def code418():
    css_style = url_for("static", filename="lab1/style.css")
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


@lab1.route("/lab1/experiment")
def experiment():
    css_style = url_for("static", filename="lab1/style.css")
    a = 10
    b = 0
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div>''' + str(a/b) + '''</div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>'''
