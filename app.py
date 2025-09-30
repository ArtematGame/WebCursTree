from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)
count = 0

@app.errorhandler(404)
def not_found(err):
    return redirect("/lab1/404")

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

@app.route("/lab1")
def lab1():
    css_style = url_for("static", filename="style.css")
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

@app.route("/lab1/web")
def web():
    css_style = url_for('static', filename='style.css')
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

@app.route("/lab1/author")
def author():
    name = "Шельмин Артём Евгеньевич"
    group = "ФБИ-31"
    faculty = "ФБ"
    css_style = url_for('static', filename='style.css')
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

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    css_style = url_for('static', filename='style.css')
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

@app.route("/lab1/counter/clear")
def clear_counter():
    global count
    count = 0
    css_style = url_for('static', filename='style.css')
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    css_style = url_for('static', filename='style.css')
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

@app.route("/lab1/experiment")
def experiment():
    css_style = url_for('static', filename='style.css')
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

@app.errorhandler(500)
def not_found2(err):
    css_style = url_for('static', filename='style.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css_style + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <div class='error1'>Внутренняя ошибка сервера! Сервер перегружен, либо произошла ошибка.</div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
          </body>
        </html>''', 500

@app.route('/lab2/a')
def a():
    css_style = url_for('static', filename='main.css')
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h2>Без слэша</h2>
                <br>
                <a href="/lab2/">Список заданий</a>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2025</footer>
            </body>
        </html>
        '''

@app.route('/lab2/a/')
def a2():
    css_style = url_for('static', filename='main.css')
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h2>Со слэшем</h2>
                <br>
                <a href="/lab2/">Список заданий</a>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2025</footer>
            </body>
        </html>
        '''

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    css_style = url_for('static', filename='main.css')
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return '''<!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css_style + '''">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                цветок:  ''' + flower_list[flower_id] + '''
                <br>
                <a href="/lab2/flowers/">Список цветов</a>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>'''

@app.route('/lab2/add_flower/<name>')
def add_flowers(name):
    css_style = url_for('static', filename='main.css')
    flower_list.append(name)
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h1> Добавлен новый цветок</h1>
                <p>Название нового цветка: {name} </p>
                <p>Всего цветов: {len(flower_list)}</p>
                <p>Полный список: {flower_list}</p>
                <br>
                <a href="/lab2/flowers/">Список цветов</a>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>
        '''

@app.route('/lab2/add_flower/')
def add_flower_empty():
    css_style = url_for('static', filename='main.css')
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h2>Ошибка 400</h2>
                <p>Вы не задали имя цветка</p>
                <br>
                <a href="/lab2/flowers/">Список цветов</a>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>
        ''', 400

@app.route('/lab2/flowers/')
def all_flowers():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    return render_template('flowers.html', flowers=flower_list, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    flower_list.extend(['роза', 'тюльпан', 'незабудка', 'ромашка'])
    return redirect('/lab2/flowers/')

@app.route('/lab2/example')
def example():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', 
                          name=name, lab_number=lab_number, group=group, 
                          course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    return render_template('lab2.html', 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)

@app.route('/lab2/filters')
def filters():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    css_style = url_for('static', filename='main.css')
    sum = a+b
    min = a-b
    umn = a*b
    dil = a/b
    ste = a**b
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                <h2>Калькулятор</h2>
                <div>
                Сложение: {sum}
                <br>
                Вычитание: {min}
                <br>
                Умножение: {umn}
                <br>
                Деление: {dil}
                <br>
                Возведение в степень: {ste}
                <br>
                <a href="/lab2/">Список заданий</a>
                </div>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2025</footer>
            </body>
        </html>
        '''

@app.route('/lab2/books')
def books():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    books_list = [
        {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
        {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
        {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказ', 'pages': 350},
        {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
        {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
        {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
        {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
        {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
        {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
        {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 128}
    ]
    
    return render_template('books.html', books=books_list, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)

@app.route('/lab2/fruits')
def fruits_with_images():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    fruits = [
        {'name': 'Яблоко', 'description': 'Сочный сладкий фрукт', 'image': 'apple.jpg'},
        {'name': 'Банан', 'description': 'Энергетический фрукт желтого цвета', 'image': 'banana.jpg'},
        {'name': 'Апельсин', 'description': 'Цитрусовый фрукт богатый витамином C', 'image': 'orange.jpg'},
        {'name': 'Клубника', 'description': 'Ароматная красная ягода', 'image': 'strawberry.jpg'},
        {'name': 'Виноград', 'description': 'Сладкие ягоды растущие гроздьями', 'image': 'grape.jpeg'},
        {'name': 'Ананас', 'description': 'Тропический фрукт с колючей кожурой', 'image': 'pineapple.jpg'},
        {'name': 'Манго', 'description': 'Сладкий тропический фрукт', 'image': 'mango.jpg'},
        {'name': 'Киви', 'description': 'Фрукт с зеленой мякотью и мелкими семенами', 'image': 'kiwi.jpg'},
        {'name': 'Груша', 'description': 'Сладкий фрукт грушевидной формы', 'image': 'pear.jpg'},
        {'name': 'Персик', 'description': 'Ароматный фрукт с бархатной кожурой', 'image': 'peach.jpg'},
        {'name': 'Слива', 'description': 'Небольшой фрукт фиолетового цвета', 'image': 'plum.jpeg'},
        {'name': 'Вишня', 'description': 'Маленькие красные ягоды', 'image': 'cherry.jpg'},
        {'name': 'Черешня', 'description': 'Сладкие крупные ягоды', 'image': 'sweet_cherry.png'},
        {'name': 'Лимон', 'description': 'Кислый цитрусовый фрукт', 'image': 'lemon.jpg'},
        {'name': 'Грейпфрут', 'description': 'Крупный горьковатый цитрус', 'image': 'grapefruit.jpg'},
        {'name': 'Арбуз', 'description': 'Большая сладкая ягода', 'image': 'watermelon.jpg'},
        {'name': 'Дыня', 'description': 'Сладкий ароматный фрукт', 'image': 'melon.jpg'},
        {'name': 'Гранат', 'description': 'Фрукт с множеством сочных зёрен', 'image': 'pomegranate.jpg'},
        {'name': 'Инжир', 'description': 'Сладкий фрукт с мелкими семенами', 'image': 'fig.jpg'},
        {'name': 'Хурма', 'description': 'Оранжевый сладкий фрукт', 'image': 'persimmon.jpg'}
    ]
    
    return render_template('fruits.html', fruits=fruits, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)
