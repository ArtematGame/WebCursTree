from flask import Blueprint, render_template, request, redirect, url_for, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    if x2 == '0':
        return render_template('lab4/div.html', error='Делить на ноль нельзя!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0

    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('lab4/mult-form.html')

@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1

    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods = ['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю!')

    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    
    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        if tree_count < 10:
            tree_count += 1
    
    return redirect('/lab4/tree')

users = [
    {'login': 'alexa', 'password': '123', 'name': 'Алекса Силфон', 'sex': 'Ж'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Марли', 'sex': 'М'},
    {'login': 'artem', 'password': '331', 'name': 'Артём Шельмин', 'sex': 'М'},
    {'login': 'agentmatvey', 'password': '007', 'name': 'Матвей Цеунов', 'sex': 'М'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            # Находим пользователя и получаем его данные
            user_data = None
            for user in users:
                if user['login'] == login:
                    user_data = user
            name = user_data['name'] if user_data else login
            sex = user_data['sex'] if user_data else 'Не указан'
        else:
            authorized = False
            login = ''
            name = ''
            sex = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name, sex=sex)

    login = request.form.get('login', '')
    password = request.form.get('password', '')

    # Проверка на пустые значения
    if not login and not password:
        error = 'Не введён логин и пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    elif not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    elif not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    # Проверка логина и пароля
    user_data = None
    for user in users:
        if user['login'] == login and user['password'] == password:
            user_data = user

    if user_data:
        session['login'] = login
        return redirect('/lab4/login')
    else:
        error = 'Неверны логин и/или пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temp = request.form.get('temp')
    
    if not temp:
        return render_template('lab4/fridge.html', error="Ошибка: не задана температура")
    
    temp = int(temp)
    
    if temp < -12:
        return render_template('lab4/fridge.html', error="Не удалось установить температуру — слишком низкое значение")
    if temp > -1:
        return render_template('lab4/fridge.html', error="Не удалось установить температуру — слишком высокое значение")
    
    if temp >= -12 and temp <= -9:
        snow = "❄️❄️❄️"
    elif temp >= -8 and temp <= -5:
        snow = "❄️❄️"
    else:
        snow = "❄️"
    
    result = f"Установлена температура: {temp}°C {snow}"
    return render_template('lab4/fridge.html', result=result)

@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')
    
    grain_type = request.form.get('grain')
    weight = request.form.get('weight')
    
    if not weight:
        return render_template('lab4/grain.html', result="Ошибка: не указан вес")
    
    weight = float(weight)
    
    if weight <= 0:
        return render_template('lab4/grain.html', result="Ошибка: вес должен быть больше 0")
    
    if weight > 100:
        return render_template('lab4/grain.html', result="Ошибка: нет в наличии")
    
    # Цены за тонну
    if grain_type == 'barley':
        price = 12000
        name = 'ячмень'
    elif grain_type == 'oats':
        price = 8500
        name = 'овёс'
    elif grain_type == 'wheat':
        price = 9000
        name = 'пшеница'
    elif grain_type == 'rye':
        price = 15000
        name = 'рожь'
    else:
        return render_template('lab4/grain.html', result="Ошибка: не выбран тип зерна")
    
    total = weight * price
    
    # Скидка
    if weight > 10:
        discount = total * 0.1
        total -= discount
        result = f"Заказ успешно сформирован. Вы заказали {name}. Вес: {weight} т. Сумма: {int(total)} руб. (скидка 10%)"
    else:
        result = f"Заказ успешно сформирован. Вы заказали {name}. Вес: {weight} т. Сумма: {int(total)} руб."
    
    return render_template('lab4/grain.html', result=result)