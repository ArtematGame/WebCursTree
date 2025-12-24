from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
import sqlite3
import hashlib

rgz = Blueprint('rgz', __name__)

def get_db():
    """Получает соединение с базой данных"""
    # Используйте правильный путь к базе данных
    db_path = '/home/Artemat/WebCursTree/sqlite3/database.db'
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Хеширует пароль"""
    return hashlib.sha256(password.encode()).hexdigest()

# Основные маршруты
@rgz.route('/rgz')
def index():
    """Главная страница банка"""
    user = None
    if 'rgz_login' in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE login = ?",
            (session['rgz_login'],)
        )
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            user = dict(user_data)
    
    return render_template('rgz/index.html', user=user)

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    """Вход в банк"""
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login_input = request.form.get('login')
    password_input = request.form.get('password')
    
    if not login_input or not password_input:
        return render_template('rgz/login.html', error='Заполните все поля')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем пользователя по логину
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (login_input,)
    )
    
    user_data = cursor.fetchone()  # <-- Вот здесь получаем данные
    conn.close()
    
    if not user_data:  # <-- Проверяем, нашли ли пользователя
        return render_template('rgz/login.html', error='Неверный логин или пароль')
    
    # Преобразуем строку Row в словарь
    user = dict(user_data)
    
    # Хешируем введенный пароль для сравнения
    hashed_password = hashlib.sha256(password_input.encode()).hexdigest()
    
    # Сравниваем хеши
    if user['password'] != hashed_password:
        return render_template('rgz/login.html', error='Неверный логин или пароль')
    
    # Сохраняем в сессии
    session['rgz_login'] = user['login']
    session['rgz_user_id'] = user['id']
    session['rgz_is_manager'] = bool(user['is_manager'])
    
    return redirect('/rgz/dashboard')

@rgz.route('/rgz/logout')
def logout():
    """Выход из банка"""
    session.pop('rgz_login', None)
    session.pop('rgz_user_id', None)
    session.pop('rgz_is_manager', None)
    return render_template('rgz/logout.html')

@rgz.route('/rgz/dashboard')
def dashboard():
    """Личный кабинет"""
    if 'rgz_login' not in session:
        return render_template('rgz/login.html', error='Требуется авторизация')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (session['rgz_login'],)
    )
    
    user_data = cursor.fetchone()
    conn.close()
    
    if not user_data:
        return render_template('rgz/login.html', error='Пользователь не найден')
    
    user = dict(user_data)
    
    return render_template('rgz/dashboard.html', user=user)

@rgz.route('/rgz/transfer', methods=['GET', 'POST'])
def transfer():
    """Перевод денег"""
    if 'rgz_login' not in session:
        return render_template('rgz/login.html', error='Требуется авторизация')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем текущего пользователя
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (session['rgz_login'],)
    )
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return render_template('rgz/login.html', error='Пользователь не найден')
    
    user = dict(user_data)
    
    if request.method == 'GET':
        conn.close()
        return render_template('rgz/transfer.html', user=user)
    
    # Обработка перевода
    to_account = request.form.get('to_account')
    amount = request.form.get('amount')
    description = request.form.get('description', '')
    
    if not to_account or not amount:
        conn.close()
        return render_template('rgz/transfer.html', user=user, error='Заполните все обязательные поля')
    
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except:
        conn.close()
        return render_template('rgz/transfer.html', user=user, error='Неверная сумма')
    
    # Проверяем баланс
    if user['balance'] < amount:
        conn.close()
        return render_template('rgz/transfer.html', user=user, error='Недостаточно средств')
    
    # Ищем получателя
    cursor.execute(
        "SELECT * FROM users WHERE account = ?",
        (to_account,)
    )
    
    recipient_data = cursor.fetchone()
    if not recipient_data:
        conn.close()
        return render_template('rgz/transfer.html', user=user, error='Получатель не найден')
    
    recipient = dict(recipient_data)
    
    if recipient['id'] == user['id']:
        conn.close()
        return render_template('rgz/transfer.html', user=user, error='Нельзя перевести самому себе')
    
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
    
    # Записываем транзакцию (если есть таблица transactions)
    try:
        cursor.execute(
            "INSERT INTO transactions (from_account, to_account, amount, description) VALUES (?, ?, ?, ?)",
            (user['account'], recipient['account'], amount, description)
        )
    except:
        pass  # Если таблицы нет, просто пропускаем
    
    conn.commit()
    conn.close()
    
    # Обновляем баланс пользователя для отображения
    user['balance'] = new_sender_balance
    
    return render_template('rgz/success.html', 
                         message=f'Перевод на сумму {amount} руб. выполнен успешно!',
                         login=user['login'])

@rgz.route('/rgz/transactions')
def transactions():
    """История транзакций"""
    if 'rgz_login' not in session:
        return render_template('rgz/login.html', error='Требуется авторизация')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем текущего пользователя
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (session['rgz_login'],)
    )
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return render_template('rgz/login.html', error='Пользователь не найден')
    
    user = dict(user_data)
    
    # Получаем транзакции (если таблица есть)
    try:
        cursor.execute(
            "SELECT * FROM transactions WHERE from_account = ? OR to_account = ? ORDER BY created_at DESC",
            (user['account'], user['account'])
        )
        transactions_data = cursor.fetchall()
        transactions = [dict(t) for t in transactions_data]
    except:
        transactions = []
    
    conn.close()
    
    return render_template('rgz/transactions.html', user=user, transactions=transactions)

@rgz.route('/rgz/manage')
def manage():
    """Управление пользователями (для менеджеров)"""
    if 'rgz_login' not in session or not session.get('rgz_is_manager'):
        return render_template('rgz/login.html', error='Требуется авторизация менеджера')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем текущего пользователя
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (session['rgz_login'],)
    )
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return render_template('rgz/login.html', error='Пользователь не найден')
    
    user = dict(user_data)
    
    # Получаем всех пользователей
    cursor.execute(
        "SELECT id, full_name, login, phone, account, balance, is_manager FROM users ORDER BY id"
    )
    
    users_data = cursor.fetchall()
    all_users = [dict(u) for u in users_data]
    
    conn.close()
    
    return render_template('rgz/manage.html', user=user, users=all_users)

@rgz.route('/rgz/create_user', methods=['GET', 'POST'])
def create_user():
    """Создание пользователя (для менеджеров)"""
    if 'rgz_login' not in session or not session.get('rgz_is_manager'):
        return render_template('rgz/login.html', error='Требуется авторизация менеджера')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Получаем текущего пользователя
    cursor.execute(
        "SELECT * FROM users WHERE login = ?",
        (session['rgz_login'],)
    )
    
    user_data = cursor.fetchone()
    if not user_data:
        conn.close()
        return render_template('rgz/login.html', error='Пользователь не найден')
    
    user = dict(user_data)
    
    if request.method == 'GET':
        conn.close()
        return render_template('rgz/create_user.html', user=user)
    
    # Обработка создания пользователя
    full_name = request.form.get('full_name')
    login = request.form.get('login')
    password = request.form.get('password')
    phone = request.form.get('phone')
    is_manager = request.form.get('is_manager') == 'on'
    
    # Проверяем обязательные поля
    if not all([full_name, login, password]):
        conn.close()
        return render_template('rgz/create_user.html', user=user,
                             error='Заполните все обязательные поля')
    
    # Проверяем, существует ли логин
    cursor.execute(
        "SELECT id FROM users WHERE login = ?",
        (login,)
    )
    
    if cursor.fetchone():
        conn.close()
        return render_template('rgz/create_user.html', user=user,
                             error='Пользователь с таким логином уже существует')
    
    # Хешируем пароль
    password_hash = hash_password(password)
    
    # Генерируем номер счета
    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()[0]
    account = f'ACC{count + 100:03d}'
    
    # Баланс по умолчанию
    balance = 1000 if not is_manager else 0
    
    # Создаем нового пользователя
    cursor.execute(
        """INSERT INTO users (full_name, login, password, phone, account, balance, is_manager) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (full_name, login, password_hash, phone, account, balance, is_manager)
    )
    
    conn.commit()
    conn.close()
    
    return render_template('rgz/success.html', 
                         message=f'Пользователь {full_name} успешно создан!',
                         login=user['login'])

# JSON-RPC API
@rgz.route('/rgz/api', methods=['POST'])
def api():
    """Простой JSON-RPC API"""
    try:
        data = request.get_json()
        method = data.get('method')
        
        if method == 'get_balance':
            if 'rgz_login' not in session:
                return jsonify({'error': 'Unauthorized'})
            
            conn = get_db()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT balance FROM users WHERE login = ?",
                (session['rgz_login'],)
            )
            
            user_data = cursor.fetchone()
            conn.close()
            
            if not user_data:
                return jsonify({'error': 'User not found'})
            
            return jsonify({'result': user_data['balance']})
        
        elif method == 'transfer':
            if 'rgz_login' not in session:
                return jsonify({'error': 'Unauthorized'})
            
            conn = get_db()
            cursor = conn.cursor()
            
            # Получаем отправителя
            cursor.execute(
                "SELECT * FROM users WHERE login = ?",
                (session['rgz_login'],)
            )
            
            user_data = cursor.fetchone()
            if not user_data:
                conn.close()
                return jsonify({'error': 'User not found'})
            
            user = dict(user_data)
            
            params = data.get('params', {})
            to_account = params.get('to_account')
            amount = params.get('amount')
            
            # Простая проверка
            if not to_account or not amount:
                conn.close()
                return jsonify({'error': 'Missing parameters'})
            
            try:
                amount = float(amount)
            except:
                conn.close()
                return jsonify({'error': 'Invalid amount'})
            
            # Ищем получателя
            cursor.execute(
                "SELECT * FROM users WHERE account = ?",
                (to_account,)
            )
            
            recipient_data = cursor.fetchone()
            if not recipient_data:
                conn.close()
                return jsonify({'error': 'Recipient not found'})
            
            recipient = dict(recipient_data)
            
            if recipient['id'] == user['id']:
                conn.close()
                return jsonify({'error': 'Cannot transfer to yourself'})
            
            if user['balance'] < amount:
                conn.close()
                return jsonify({'error': 'Insufficient funds'})
            
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
            description = params.get('description', '')
            try:
                cursor.execute(
                    "INSERT INTO transactions (from_account, to_account, amount, description) VALUES (?, ?, ?, ?)",
                    (user['account'], recipient['account'], amount, description)
                )
            except:
                pass
            
            conn.commit()
            conn.close()
            
            return jsonify({'result': 'Transfer successful'})
        
        else:
            return jsonify({'error': 'Method not found'})
            
    except Exception as e:
        return jsonify({'error': str(e)})