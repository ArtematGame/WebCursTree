from flask import Blueprint, render_template, request, redirect, session, jsonify
import sqlite3
import hashlib

rgz = Blueprint('rgz', __name__)

def get_db():
    db_path = '/home/Artemat/WebCursTree/sqlite3/database.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def get_user():
    if 'rgz_login' not in session:
        return None
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login = ?", (session['rgz_login'],))
    user = cur.fetchone()
    conn.close()
    return dict(user) if user else None

# HTML страницы
@rgz.route('/rgz')
def index():
    return render_template('rgz/index.html', user=get_user())

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    return redirect('/rgz')

@rgz.route('/rgz/dashboard')
def dashboard():
    user = get_user()
    return render_template('rgz/dashboard.html', user=user) if user else redirect('/rgz/login')

@rgz.route('/rgz/transfer')
def transfer_page():
    user = get_user()
    return render_template('rgz/transfer.html', user=user) if user else redirect('/rgz/login')

@rgz.route('/rgz/transactions')
def transactions_page():
    user = get_user()
    return render_template('rgz/transactions.html', user=user) if user else redirect('/rgz/login')

@rgz.route('/rgz/manage')
def manage_page():
    user = get_user()
    if not user or not user['is_manager']:
        return redirect('/rgz/login')
    return render_template('rgz/manage.html', user=user)

@rgz.route('/rgz/create_user')
def create_user_page():
    user = get_user()
    if not user or not user['is_manager']:
        return redirect('/rgz/login')
    return render_template('rgz/create_user.html', user=user)

@rgz.route('/rgz/logout')
def logout():
    session.clear()
    return redirect('/rgz')

# JSON-RPC API (главное по заданию)
@rgz.route('/rgz/api', methods=['POST'])
def api():
    try:
        data = request.get_json()
        method = data.get('method')
        params = data.get('params', {})
        req_id = data.get('id', 1)
        
        # Авторизация
        if method == 'auth.login':
            login = params.get('login')
            password = params.get('password')
            if not login or not password:
                return error_response('Missing credentials', req_id)
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE login = ?", (login,))
            user = cur.fetchone()
            conn.close()
            
            if not user or hash_password(password) != dict(user)['password']:
                return error_response('Invalid login/password', req_id)
            
            user_dict = dict(user)
            session['rgz_login'] = user_dict['login']
            session['rgz_is_manager'] = user_dict['is_manager']
            
            return json_response({'success': True, 'user': user_dict['login']}, req_id)
        
        # Проверка авторизации для остальных методов
        if 'rgz_login' not in session:
            return error_response('Unauthorized', req_id)
        
        user = get_user()
        
        # Баланс
        if method == 'user.get_balance':
            return json_response({'balance': user['balance']}, req_id)
        
        # Информация о пользователе
        elif method == 'user.get_info':
            user_copy = user.copy()
            user_copy.pop('password', None)
            return json_response({'user': user_copy}, req_id)
        
        # Перевод
        elif method == 'transfer':
            to_acc = params.get('to_account')
            amount = params.get('amount')
            desc = params.get('description', '')
            
            if not to_acc or not amount:
                return error_response('Missing parameters', req_id)
            
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError
            except:
                return error_response('Invalid amount', req_id)
            
            if user['balance'] < amount:
                return error_response('Insufficient funds', req_id)
            
            conn = get_db()
            cur = conn.cursor()
            
            # Ищем получателя
            cur.execute("SELECT * FROM users WHERE account = ? OR phone = ?", (to_acc, to_acc))
            recipient = cur.fetchone()
            if not recipient:
                conn.close()
                return error_response('Recipient not found', req_id)
            
            recipient = dict(recipient)
            if recipient['id'] == user['id']:
                conn.close()
                return error_response('Cannot transfer to yourself', req_id)
            
            # Выполняем перевод
            new_sender = user['balance'] - amount
            new_recipient = recipient['balance'] + amount
            
            cur.execute("UPDATE users SET balance = ? WHERE id = ?", (new_sender, user['id']))
            cur.execute("UPDATE users SET balance = ? WHERE id = ?", (new_recipient, recipient['id']))
            
            # История операций
            try:
                cur.execute("INSERT INTO transactions (from_account, to_account, amount, description) VALUES (?, ?, ?, ?)",
                          (user['account'], recipient['account'], amount, desc))
            except:
                pass
            
            conn.commit()
            conn.close()
            
            return json_response({'success': True, 'new_balance': new_sender}, req_id)
        
        # История операций
        elif method == 'transactions.get':
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute("SELECT * FROM transactions WHERE from_account = ? OR to_account = ? ORDER BY created_at DESC",
                          (user['account'], user['account']))
                transactions = [dict(t) for t in cur.fetchall()]
            except:
                transactions = []
            conn.close()
            return json_response({'transactions': transactions}, req_id)
        
        # Менеджерские методы
        elif method == 'users.get_all':
            if not user['is_manager']:
                return error_response('Manager access required', req_id)
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT id, full_name, login, phone, account, balance, is_manager FROM users")
            users = [dict(u) for u in cur.fetchall()]
            conn.close()
            return json_response({'users': users}, req_id)
        
        elif method == 'user.create':
            if not user['is_manager']:
                return error_response('Manager access required', req_id)
            
            name = params.get('full_name')
            login = params.get('login')
            pwd = params.get('password')
            phone = params.get('phone', '')
            is_manager = params.get('is_manager', False)
            
            if not name or not login or not pwd:
                return error_response('Missing required fields', req_id)
            
            conn = get_db()
            cur = conn.cursor()
            
            # Проверка существования логина
            cur.execute("SELECT id FROM users WHERE login = ?", (login,))
            if cur.fetchone():
                conn.close()
                return error_response('Login already exists', req_id)
            
            # Генерация счета
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
            account = f'ACC{count + 100:03d}'
            balance = 1000 if not is_manager else 0
            
            cur.execute("INSERT INTO users (full_name, login, password, phone, account, balance, is_manager) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (name, login, hash_password(pwd), phone, account, balance, is_manager))
            
            conn.commit()
            conn.close()
            return json_response({'success': True, 'account': account}, req_id)
        
        else:
            return error_response('Method not found', req_id)
            
    except Exception as e:
        return error_response(f'Server error: {str(e)}', data.get('id', 1) if 'data' in locals() else 1)

def json_response(result, req_id):
    return jsonify({'jsonrpc': '2.0', 'result': result, 'id': req_id})

def error_response(message, req_id):
    return jsonify({'jsonrpc': '2.0', 'error': {'code': -32000, 'message': message}, 'id': req_id})