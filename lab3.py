from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай – 80 рублей, зелёный – 70 рублей.
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара – на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)
    
@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    line_height = request.args.get('line_height')
    
    if color or bg_color or font_size or line_height:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if line_height:
            resp.set_cookie('line_height', line_height)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    line_height = request.cookies.get('line_height')
    return render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, line_height=line_height)

@lab3.route('/lab3/settings_clear')
def settings_clear():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('line_height')
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket.html')

@lab3.route('/lab3/ticket_result')
def ticket_result():
    price = 0
    
    # Взрослый билет стоит 1000 руб, детский — 700 руб.
    age = int(request.args.get('age'))
    if age < 18:
        price = 700
        is_child = True
    else:
        price = 1000
        is_child = False

    # Если полка нижняя или нижняя боковая, то к стоимости добавляется ещё 100 руб.
    shelf = request.args.get('shelf')
    if shelf == 'lower' or shelf == 'lower_side':
        price += 100

    # Бельё увеличивает стоимость на 75 рублей.
    if request.args.get('linen') == 'on':
        price += 75

    # Если есть багаж, то стоимость увеличивается на 250 руб.
    if request.args.get('luggage') == 'on':
        price += 250

    # Страховка увеличивает стоимость на 150 руб.
    if request.args.get('insurance') == 'on':
        price += 150

    return render_template('lab3/ticket_result.html', price=price, is_child=is_child,
                         fio=request.args.get('fio'), age=age,
                         departure=request.args.get('departure'),
                         destination=request.args.get('destination'),
                         travel_date=request.args.get('travel_date'))

products = [
    {"name": "iPhone 15", "price": 999, "brand": "Apple", "color": "черный"},
    {"name": "Samsung S24", "price": 899, "brand": "Samsung", "color": "белый"},
    {"name": "Xiaomi Note 13", "price": 299, "brand": "Xiaomi", "color": "синий"},
    {"name": "Google Pixel 8", "price": 799, "brand": "Google", "color": "серый"},
    {"name": "OnePlus 12", "price": 699, "brand": "OnePlus", "color": "зеленый"},
    {"name": "Huawei P60", "price": 749, "brand": "Huawei", "color": "золотой"},
    {"name": "Nokia G50", "price": 249, "brand": "Nokia", "color": "синий"},
    {"name": "Realme GT 3", "price": 449, "brand": "Realme", "color": "белый"},
    {"name": "Oppo Find X6", "price": 799, "brand": "Oppo", "color": "черный"},
    {"name": "Vivo X100", "price": 699, "brand": "Vivo", "color": "красный"},
    {"name": "Motorola Edge 40", "price": 549, "brand": "Motorola", "color": "зеленый"},
    {"name": "Honor Magic 5", "price": 649, "brand": "Honor", "color": "серебристый"},
    {"name": "Asus Zenfone 10", "price": 729, "brand": "Asus", "color": "синий"},
    {"name": "LG Velvet", "price": 399, "brand": "LG", "color": "белый"},
    {"name": "ZTE Axon 40", "price": 499, "brand": "ZTE", "color": "черный"},
    {"name": "Alcatel 3X", "price": 179, "brand": "Alcatel", "color": "синий"},
    {"name": "Tecno Camon 20", "price": 199, "brand": "Tecno", "color": "зеленый"},
    {"name": "Infinix Note 30", "price": 219, "brand": "Infinix", "color": "золотой"},
    {"name": "Poco X5", "price": 279, "brand": "Poco", "color": "черный"},
    {"name": "iPhone 14", "price": 799, "brand": "Apple", "color": "фиолетовый"}
]

@lab3.route('/lab3/products')
def products_search():
    prices = [p['price'] for p in products]
    min_all = min(prices)
    max_all = max(prices)

    if request.args.get('reset'):
        resp = make_response(redirect('/lab3/products'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    min_price = request.args.get('min_price') or request.cookies.get('min_price', '')
    max_price = request.args.get('max_price') or request.cookies.get('max_price', '')

    if request.args.get('min_price') is not None:
        resp = make_response(redirect('/lab3/products'))
        resp.set_cookie('min_price', min_price)
        resp.set_cookie('max_price', max_price)
        return resp

    filtered_products = products
    
    if min_price or max_price:
        min_val = float(min_price) if min_price else min_all
        max_val = float(max_price) if max_price else max_all
        
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        
        filtered_products = [p for p in products if min_val <= p['price'] <= max_val]
    
    return render_template('lab3/products.html', 
                         products=filtered_products,
                         min_price=min_price,
                         max_price=max_price,
                         min_all=min_all,
                         max_all=max_all)

