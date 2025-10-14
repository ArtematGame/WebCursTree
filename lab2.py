from flask import Blueprint, url_for, request, redirect, abort, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a():
    css_style = url_for('static', filename='lab1/main.css')
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                <div>
                    <h2>Без слэша</h2>
                    <br>
                    <a href="/lab2">Список заданий</a>
                </div>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2025</footer>
            </body>
        </html>
        '''


@lab2.route('/lab2/a/')
def a2():
    css_style = url_for('static', filename='lab1/main.css')
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                <div>
                    <h2>Со слэшем</h2>
                    <br>
                    <a href="/lab2">Список заданий</a>
                </div>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2025</footer>
            </body>
        </html>
        '''


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']


@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    css_style = url_for('static', filename='lab1/main.css')
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return '''<!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css_style + '''">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                <div>
                    цветок:  ''' + flower_list[flower_id] + '''
                    <br>
                    <a href="/lab2/flowers/">Список цветов</a>
                </div>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>'''


@lab2.route('/lab2/add_flower/<name>')
def add_flowers(name):
    css_style = url_for('static', filename='lab1/main.css')
    flower_list.append(name)
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                <h1> Добавлен новый цветок</h1>
                <div>
                    <p>Название нового цветка: {name} </p>
                    <p>Всего цветов: {len(flower_list)}</p>
                    <p>Полный список: {flower_list}</p>
                    <br>
                    <a href="/lab2/flowers/">Список цветов</a>
                </div>
                <footer>&copy; Шельмин Артём, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>
        '''


@lab2.route('/lab2/add_flower/')
def add_flower_empty():
    css_style = url_for('static', filename='lab1/main.css')
    return f'''
        <!doctype html>
        <html>
        <link rel="stylesheet" href="{css_style}">
            <body>
                <title>НГТУ, ФБ, Лабораторная работа 2</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                <div>
                    <h2>Ошибка 400</h2>
                    <p>Вы не задали имя цветка</p>
                    <br>
                    <a href="/lab2/flowers/">Список цветов</a>
                </div>
                <footer>Шельмин Артём Евгеньевич, ФБИ-31, 3 курс, 2024</footer>
            </body>
        </html>
        ''', 400


@lab2.route('/lab2/flowers/')
def all_flowers():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    return render_template('lab2/flowers.html', flowers=flower_list, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    flower_list.extend(['роза', 'тюльпан', 'незабудка', 'ромашка'])
    return redirect('/lab2/flowers/')


@lab2.route('/lab2/example')
def example():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', 
                          name=name, lab_number=lab_number, group=group, 
                          course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    return render_template('lab2/lab2.html', 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)


@lab2.route('/lab2/filters')
def filters():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    css_style = url_for('static', filename='lab1/main.css')
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
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
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


@lab2.route('/lab2/books')
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
    
    return render_template('lab2/books.html', books=books_list, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)


@lab2.route('/lab2/fruits')
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
    
    return render_template('lab2/fruits.html', fruits=fruits, 
                          name=name, lab_number=lab_number, group=group, 
                          course=course)


flowers_with_prices = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330}
]

@lab2.route('/lab2/flowers_advanced/', methods=['GET', 'POST'])
def flowers_advanced():
    name, lab_number, group, course = 'Шельмин Артём', '2', 'ФБИ-31', '3'

    if request.method == 'POST':
        flower_name = request.form.get('flower_name')
        flower_price = request.form.get('flower_price')
        flowers_with_prices.append({'name': flower_name, 'price': int(flower_price)})
    return render_template('lab2/flowers_advanced.html', flowers=flowers_with_prices, name=name, lab_number=lab_number, group=group, course=course)


@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id >= len(flowers_with_prices):
        abort(404)
    flowers_with_prices.pop(flower_id)
    return redirect('/lab2/flowers_advanced/')


@lab2.route('/lab2/del_all_flowers')
def del_all_flowers():
    flowers_with_prices.clear()
    return redirect('/lab2/flowers_advanced/')
