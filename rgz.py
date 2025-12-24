from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='artem_shelmin_knowledge_base',
            user='artem_shelmin_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# База данных в памяти для простоты
bank_data = {
    'users': [
        # Менеджеры
        {'id': 1, 'full_name': 'Иванов Иван', 'login': 'admin', 'password': 'admin123', 
         'phone': '+79001112233', 'account': 'ADMIN001', 'balance': 0, 'is_manager': True},
        {'id': 2, 'full_name': 'Сидорова Анна', 'login': 'client1', 'password': 'client123', 
         'phone': '+79003334455', 'account': 'ACC001', 'balance': 1000, 'is_manager': False},
        {'id': 3, 'full_name': 'Кузнецов Сергей', 'login': 'client2', 'password': 'client123', 
         'phone': '+79004445566', 'account': 'ACC002', 'balance': 1000, 'is_manager': False},
        {'id': 4, 'full_name': 'Смирнова Ольга', 'login': 'client3', 'password': 'client123', 
         'phone': '+79005556677', 'account': 'ACC003', 'balance': 1000, 'is_manager': False},
        {'id': 5, 'full_name': 'Васильев Дмитрий', 'login': 'client4', 'password': 'client123', 
         'phone': '+79006667788', 'account': 'ACC004', 'balance': 1000, 'is_manager': False},
        {'id': 6, 'full_name': 'Николаева Елена', 'login': 'client5', 'password': 'client123', 
         'phone': '+79007778899', 'account': 'ACC005', 'balance': 1000, 'is_manager': False},
        {'id': 7, 'full_name': 'Алексеев Алексей', 'login': 'client6', 'password': 'client123', 
         'phone': '+79008889900', 'account': 'ACC006', 'balance': 1000, 'is_manager': False},
        {'id': 8, 'full_name': 'Павлова Мария', 'login': 'client7', 'password': 'client123', 
         'phone': '+79009990011', 'account': 'ACC007', 'balance': 1000, 'is_manager': False},
        {'id': 9, 'full_name': 'Федоров Андрей', 'login': 'client8', 'password': 'client123', 
         'phone': '+79001001122', 'account': 'ACC008', 'balance': 1000, 'is_manager': False},
        {'id': 10, 'full_name': 'Соколова Виктория', 'login': 'client9', 'password': 'client123', 
         'phone': '+79001112233', 'account': 'ACC009', 'balance': 1000, 'is_manager': False},
        {'id': 11, 'full_name': 'Лебедев Максим', 'login': 'client10', 'password': 'client123', 
         'phone': '+79001223344', 'account': 'ACC010', 'balance': 1000, 'is_manager': False},
    ],
    'transactions': []
}

# Основные маршруты
@rgz.route('/rgz')
def index():
    # Главная страница банка
    user = None
    if 'rgz_login' in session:
        for u in bank_data['users']:
            if u['login'] == session['rgz_login']:
                user = u
                break
    
    return render_template('rgz/index.html', user=user)

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    # Вход в банк (используем ваш шаблон из lab9)
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    # Ищем пользователя
    user = None
    for u in bank_data['users']:
        if u['login'] == login and u['password'] == password:
            user = u
            break
    
    if not user:
        return render_template('rgz/login.html', error='Неверный логин или пароль')
    
    # Сохраняем в сессии
    session['rgz_login'] = user['login']
    session['rgz_user_id'] = user['id']
    session['rgz_is_manager'] = user['is_manager']
    
    return render_template('rgz/success_login.html', login=login)

@rgz.route('/rgz/logout')
def logout():
    # Выход из банка
    session.pop('rgz_login', None)
    session.pop('rgz_user_id', None)
    session.pop('rgz_is_manager', None)
    return render_template('rgz/logout.html')

@rgz.route('/rgz/dashboard')
def dashboard():
    # Личный кабинет
    if 'rgz_login' not in session:
        return render_template('rgz/login.html', error='Требуется авторизация')
    
    # Находим пользователя
    user = None
    for u in bank_data['users']:
        if u['login'] == session['rgz_login']:
            user = u
            break
    
    if not user:
        return render_template('rgz/login.html', error='Пользователь не найден')
    
    return render_template('rgz/dashboard.html', user=user)

@rgz.route('/rgz/transfer', methods=['GET', 'POST'])
def transfer():
    # Перевод денег
    if 'rgz_login' not in session:
        return render_template('rgz/login.html', error='Требуется авторизация')
    
    # Находим пользователя
    user = None
    for u in bank_data['users']:
        if u['login'] == session['rgz_login']:
            user = u
            break
    
    if request.method == 'GET':
        return render_template('rgz/transfer.html', user=user)
    
    # Обработка перевода
    to_account = request.form.get('to_account')
    amount = request.form.get('amount')
    
    if not to_account or not amount:
        return render_template('rgz/transfer.html', user=user, error='Заполните все поля')
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except:
        return render_template('rgz/transfer.html', user=user, error='Неверная сумма')
    
    # Проверяем баланс
    if user['balance'] < amount:
        return render_template('rgz/transfer.html', user=user, error='Недостаточно средств')
    
    # Ищем получателя
    recipient = None
    for u in bank_data['users']:
        if u['account'] == to_account or u['phone'] == to_account:
            recipient = u
            break
    
    if not recipient:
        return render_template('rgz/transfer.html', user=user, error='Получатель не найден')
    
    if recipient['id'] == user['id']:
        return render_template('rgz/transfer.html', user=user, error='Нельзя перевести самому себе')
    
    # Выполняем перевод
    user['balance'] -= amount
    recipient['balance'] += amount
    
    # Записываем транзакцию
    transaction = {
        'id': len(bank_data['transactions']) + 1,
        'from_account': user['account'],
        'to_account': recipient['account'],
        'amount': amount,
        'description': request.form.get('description', '')
    }
    bank_data['transactions'].append(transaction)
    
    return render_template('rgz/success.html', 
                         message=f'Перевод на сумму {amount} руб. выполнен успешно!',
                         login=user['login'])

@rgz.route('/rgz/transactions')
def transactions():
    # История транзакций
    if 'rgz_login' not in session:
        return render_template('rgz/login.html', error='Требуется авторизация')
    
    # Находим пользователя
    user = None
    for u in bank_data['users']:
        if u['login'] == session['rgz_login']:
            user = u
            break
    
    # Фильтруем транзакции пользователя
    user_transactions = []
    for t in bank_data['transactions']:
        if t['from_account'] == user['account'] or t['to_account'] == user['account']:
            user_transactions.append(t)
    
    return render_template('rgz/transactions.html', user=user, transactions=user_transactions)

@rgz.route('/rgz/manage')
def manage():
    # Управление пользователями (для менеджеров)
    if 'rgz_login' not in session or not session.get('rgz_is_manager'):
        return render_template('rgz/login.html', error='Требуется авторизация менеджера')
    
    # Находим пользователя
    user = None
    for u in bank_data['users']:
        if u['login'] == session['rgz_login']:
            user = u
            break
    
    return render_template('rgz/manage.html', user=user, users=bank_data['users'])

@rgz.route('/rgz/create_user', methods=['GET', 'POST'])
def create_user():
    # Создание пользователя (для менеджеров)
    if 'rgz_login' not in session or not session.get('rgz_is_manager'):
        return render_template('rgz/login.html', error='Требуется авторизация менеджера')
    
    # Находим пользователя
    user = None
    for u in bank_data['users']:
        if u['login'] == session['rgz_login']:
            user = u
            break
    
    if request.method == 'GET':
        return render_template('rgz/create_user.html', user=user)
    
    # Обработка создания пользователя
    full_name = request.form.get('full_name')
    login = request.form.get('login')
    password = request.form.get('password')
    phone = request.form.get('phone')
    is_manager = request.form.get('is_manager') == 'on'
    
    # Проверяем, существует ли логин
    for u in bank_data['users']:
        if u['login'] == login:
            return render_template('rgz/create_user.html', user=user,
                                 error='Пользователь с таким логином уже существует')
    
    # Создаем нового пользователя
    new_user = {
        'id': len(bank_data['users']) + 1,
        'full_name': full_name,
        'login': login,
        'password': password,
        'phone': phone,
        'account': f'ACC{len(bank_data["users"]) + 100:03d}',
        'balance': 1000 if not is_manager else 0,
        'is_manager': is_manager
    }
    
    bank_data['users'].append(new_user)
    
    return render_template('rgz/success.html', 
                         message=f'Пользователь {full_name} успешно создан!',
                         login=user['login'])

# JSON-RPC API (максимально просто)
@rgz.route('/rgz/api', methods=['POST'])
def api():
    # Простой JSON-RPC API
    try:
        data = request.get_json()
        method = data.get('method')
        
        if method == 'get_balance':
            if 'rgz_login' not in session:
                return jsonify({'error': 'Unauthorized'})
            
            # Находим пользователя
            user = None
            for u in bank_data['users']:
                if u['login'] == session['rgz_login']:
                    user = u
                    break
            
            return jsonify({'result': user['balance']})
        
        elif method == 'transfer':
            if 'rgz_login' not in session:
                return jsonify({'error': 'Unauthorized'})
            
            # Находим пользователя
            user = None
            for u in bank_data['users']:
                if u['login'] == session['rgz_login']:
                    user = u
                    break
            
            params = data.get('params', {})
            to_account = params.get('to_account')
            amount = params.get('amount')
            
            # Простая проверка
            if not to_account or not amount:
                return jsonify({'error': 'Missing parameters'})
            
            # Ищем получателя
            recipient = None
            for u in bank_data['users']:
                if u['account'] == to_account:
                    recipient = u
                    break
            
            if not recipient:
                return jsonify({'error': 'Recipient not found'})
            
            # Выполняем перевод
            user['balance'] -= float(amount)
            recipient['balance'] += float(amount)
            
            return jsonify({'result': 'Transfer successful'})
        
        else:
            return jsonify({'error': 'Method not found'})
            
    except Exception as e:
        return jsonify({'error': str(e)})