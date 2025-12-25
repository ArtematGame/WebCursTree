from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
import sqlite3
import hashlib
import json

rgz = Blueprint('rgz', __name__)

def get_db():
    # Используйте правильный путь к базе данных
    db_path = '/home/Artemat/WebCursTree/sqlite3/database.db'
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Основные маршруты для отображения страниц
@rgz.route('/rgz')
def index():
    return render_template('rgz/index.html')

@rgz.route('/rgz/login')
def login_page():
    return render_template('rgz/login.html')

@rgz.route('/rgz/register')
def register_page():
    return render_template('rgz/register.html')

@rgz.route('/rgz/logout')
def logout():
    session.pop('rgz_login', None)
    session.pop('rgz_user_id', None)
    session.pop('rgz_is_manager', None)
    return redirect('/rgz')

@rgz.route('/rgz/dashboard')
def dashboard_page():
    return render_template('rgz/dashboard.html')

@rgz.route('/rgz/transfer')
def transfer_page():
    return render_template('rgz/transfer.html')

@rgz.route('/rgz/transactions')
def transactions_page():
    return render_template('rgz/transactions.html')

@rgz.route('/rgz/manage')
def manage_page():
    return render_template('rgz/manage.html')

@rgz.route('/rgz/create_user')
def create_user_page():
    return render_template('rgz/create_user.html')

@rgz.route('/rgz/success')
def success_page():
    message = request.args.get('message', 'Операция выполнена успешно!')
    return render_template('rgz/success.html', message=message)

# Основной JSON-RPC API endpoint
@rgz.route('/rgz/json-rpc-api/', methods=['POST'])
def json_rpc_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': -32700,
                    'message': 'Ошибка парсинга'
                },
                'id': None
            })
        
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id', 1)
        
        # Методы, не требующие авторизации
        if method == 'login':
            return handle_login(params, request_id)
        elif method == 'register':
            return handle_register(params, request_id)
        elif method == 'get_public_info':
            return handle_get_public_info(request_id)
        
        # Проверяем авторизацию для остальных методов
        if 'rgz_login' not in session:
            return jsonify({
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Не авторизован'
                },
                'id': request_id
            })
        
        # Методы, требующие авторизации
        if method == 'get_user_info':
            return handle_get_user_info(session['rgz_login'], request_id)
        elif method == 'transfer':
            return handle_transfer(session['rgz_login'], params, request_id)
        elif method == 'get_transactions':
            return handle_get_transactions(session['rgz_login'], request_id)
        elif method == 'logout':
            return handle_logout(request_id)
        
        # Методы для менеджеров
        if method == 'get_all_users':
            if not session.get('rgz_is_manager'):
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Требуются права менеджера'
                    },
                    'id': request_id
                })
            return handle_get_all_users(request_id)
        elif method == 'create_user':
            if not session.get('rgz_is_manager'):
                return jsonify({
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Требуются права менеджера'
                    },
                    'id': request_id
                })
            return handle_create_user(params, request_id)
        
        # Если метод не найден
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Метод не найден'
            },
            'id': request_id
        })
        
    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': -32603,
                'message': f'Внутренняя ошибка: {str(e)}'
            },
            'id': data.get('id', 1) if 'data' in locals() else 1
        })

# Обработчики методов
def handle_login(params, request_id):
    login = params.get('login')
    password = params.get('password')
    
    if not login or not password:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Заполните логин и пароль'
            },
            'id': request_id
        })
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (login,)
    )
    
    user_data = cursor.fetchone()
    conn.close()
    
    if not user_data:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 4,
                'message': 'Неверный логин или пароль'
            },
            'id': request_id
        })
    
    user = dict(user_data)
    password_hash = hash_password(password)
    
    if user['password'] != password_hash:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 4,
                'message': 'Неверный логин или пароль'
            },
            'id': request_id
        })
    
    # Сохраняем в сессии
    session['rgz_login'] = user['login']
    session['rgz_user_id'] = user['id']
    session['rgz_is_manager'] = bool(user['is_manager'])
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'success': True,
            'user': {
                'login': user['login'],
                'full_name': user['full_name'],
                'is_manager': bool(user['is_manager'])
            }
        },
        'id': request_id
    })

def handle_register(params, request_id):
    full_name = params.get('full_name')
    login = params.get('login')
    password = params.get('password')
    phone = params.get('phone', '')
    
    if not all([full_name, login, password]):
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Заполните все обязательные поля'
            },
            'id': request_id
        })
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем, существует ли логин
    cursor.execute(
        "SELECT id FROM users WHERE login = ?",
        (login,)
    )
    
    if cursor.fetchone():
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 5,
                'message': 'Пользователь с таким логином уже существует'
            },
            'id': request_id
        })
    
    # Хешируем пароль
    password_hash = hash_password(password)
    
    # Генерируем номер счета
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()[0]
    account = f'ACC{count + 100:03d}'
    balance = 1000.0
    
    # Создаем нового пользователя
    cursor.execute(
        """INSERT INTO users (full_name, login, password, phone, account, balance, is_manager) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (full_name, login, password_hash, phone, account, balance, 0)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'success': True,
            'message': f'Пользователь {full_name} создан успешно'
        },
        'id': request_id
    })

def handle_get_public_info(request_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем тестовых пользователей для отображения на главной
    cursor.execute(
        "SELECT login, full_name, is_manager FROM users LIMIT 3"
    )
    
    test_users = cursor.fetchall()
    conn.close()
    
    users_list = []
    for user in test_users:
        users_list.append({
            'login': user['login'],
            'full_name': user['full_name'],
            'is_manager': bool(user['is_manager'])
        })
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'test_users': users_list
        },
        'id': request_id
    })

def handle_get_user_info(login, request_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (login,)
    )
    
    user_data = cursor.fetchone()
    conn.close()
    
    if not user_data:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 6,
                'message': 'Пользователь не найден'
            },
            'id': request_id
        })
    
    user = dict(user_data)
    # Убираем пароль из ответа
    if 'password' in user:
        del user['password']
    
    user['is_manager'] = bool(user['is_manager'])
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': user,
        'id': request_id
    })

def handle_transfer(login, params, request_id):
    to_account = params.get('to_account')
    amount = params.get('amount')
    description = params.get('description', '')
    
    if not to_account or not amount:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Заполните все обязательные поля'
            },
            'id': request_id
        })
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 7,
                'message': 'Неверная сумма'
            },
            'id': request_id
        })
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем отправителя
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (login,)
    )
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 6,
                'message': 'Пользователь не найден'
            },
            'id': request_id
        })
    
    user = dict(user_data)
    
    # Проверяем баланс
    if user['balance'] < amount:
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 8,
                'message': 'Недостаточно средств'
            },
            'id': request_id
        })
    
    # Ищем получателя
    cursor.execute(
        "SELECT * FROM users WHERE account = ? OR phone = ?",
        (to_account, to_account)
    )
    
    recipient_data = cursor.fetchone()
    if not recipient_data:
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 9,
                'message': 'Получатель не найден'
            },
            'id': request_id
        })
    
    recipient = dict(recipient_data)
    
    if recipient['id'] == user['id']:
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 10,
                'message': 'Нельзя перевести самому себе'
            },
            'id': request_id
        })
    
    # Выполняем перевод
    new_sender_balance = user['balance'] - amount
    new_recipient_balance = recipient['balance'] + amount
    
    cursor.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_sender_balance, user['id'])
    )
    
    cursor.execute(
        "UPDATE users SET balance = ? WHERE id = ?",
        (new_recipient_balance, recipient['id'])
    )
    
    # Записываем транзакцию
    try:
        cursor.execute(
            "INSERT INTO transactions (from_account, to_account, amount, description) VALUES (?, ?, ?, ?)",
            (user['account'], recipient['account'], amount, description)
        )
    except Exception as e:
        print(f"Ошибка записи транзакции: {e}")
        # Можно продолжить, даже если транзакция не записалась
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'success': True,
            'message': f'Перевод на сумму {amount:.2f} руб. выполнен успешно!',
            'new_balance': new_sender_balance
        },
        'id': request_id
    })

def handle_get_transactions(login, request_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем пользователя
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (login,)
    )
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 6,
                'message': 'Пользователь не найден'
            },
            'id': request_id
        })
    
    user = dict(user_data)
    
    try:
        # Получаем транзакции
        cursor.execute(
            "SELECT * FROM transactions WHERE from_account = ? OR to_account = ? ORDER BY created_at DESC",
            (user['account'], user['account'])
        )
        transactions_data = cursor.fetchall()
        transactions = [dict(t) for t in transactions_data]
    except Exception as e:
        print(f"Ошибка получения транзакций: {e}")
        transactions = []
    
    conn.close()
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': transactions,
        'id': request_id
    })

def handle_logout(request_id):
    session.pop('rgz_login', None)
    session.pop('rgz_user_id', None)
    session.pop('rgz_is_manager', None)
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'success': True,
            'message': 'Выход выполнен успешно'
        },
        'id': request_id
    })

def handle_get_all_users(request_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, full_name, login, phone, account, balance, is_manager FROM users ORDER BY id"
    )
    
    users_data = cursor.fetchall()
    users = []
    
    for user in users_data:
        user_dict = dict(user)
        user_dict['is_manager'] = bool(user_dict['is_manager'])
        users.append(user_dict)
    
    conn.close()
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': users,
        'id': request_id
    })

def handle_create_user(params, request_id):
    full_name = params.get('full_name')
    login = params.get('login')
    password = params.get('password')
    phone = params.get('phone', '')
    is_manager = params.get('is_manager', False)
    
    if not all([full_name, login, password]):
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Заполните все обязательные поля'
            },
            'id': request_id
        })
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id FROM users WHERE login = ?",
        (login,)
    )
    
    if cursor.fetchone():
        conn.close()
        return jsonify({
            'jsonrpc': '2.0',
            'error': {
                'code': 5,
                'message': 'Пользователь с таким логином уже существует'
            },
            'id': request_id
        })
    
    password_hash = hash_password(password)
    
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()[0]
    account = f'ACC{count + 100:03d}'
    balance = 1000.0 if not is_manager else 0.0
    
    cursor.execute(
        """INSERT INTO users (full_name, login, password, phone, account, balance, is_manager) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (full_name, login, password_hash, phone, account, balance, is_manager)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'jsonrpc': '2.0',
        'result': {
            'success': True,
            'message': f'Пользователь {full_name} успешно создан!',
            'account': account
        },
        'id': request_id
    })