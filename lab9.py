from flask import Blueprint, render_template, request, redirect, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

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

# Данные для подарков (10 уникальных)
gifts = [
    {"id": 0, "message": "С Новым годом! Желаю счастья!", "image": "/static/lab9/gift1.png", "top": 15, "left": 10},
    {"id": 1, "message": "Удачи в новом году!", "image": "/static/lab9/gift2.png", "top": 25, "left": 70},
    {"id": 2, "message": "Здоровья и благополучия!", "image": "/static/lab9/gift3.png", "top": 40, "left": 20},
    {"id": 3, "message": "Исполнения всех желаний!", "image": "/static/lab9/gift4.png", "top": 10, "left": 50},
    {"id": 4, "message": "Мира и добра!", "image": "/static/lab9/gift5.png", "top": 60, "left": 80},
    {"id": 5, "message": "Творческих успехов!", "image": "/static/lab9/gift6.png", "top": 70, "left": 30},
    {"id": 6, "message": "Финансового процветания!", "image": "/static/lab9/gift7.png", "top": 35, "left": 60},
    {"id": 7, "message": "Любви и гармонии!", "image": "/static/lab9/gift8.png", "top": 65, "left": 15},
    {"id": 8, "message": "Новых интересных проектов!", "image": "/static/lab9/gift9.png", "top": 55, "left": 40},
    {"id": 9, "message": "Весёлых праздников!", "image": "/static/lab9/gift10.png", "top": 20, "left": 85}
]

@lab9.route('/lab9/')
def main():
    # Инициализация сессии для подарков
    if 'opened_boxes' not in session:
        session['opened_boxes'] = []
    
    # Получаем открытые коробки пользователя из БД
    conn, cur = db_connect()
    user_opened = []
    
    if session.get('login'):
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT box_id FROM opened_boxes WHERE user_id=%s;", (session['login'],))
        else:
            cur.execute("SELECT box_id FROM opened_boxes WHERE user_id=?;", (session['login'],))
        
        user_opened = [row['box_id'] for row in cur.fetchall()]
        session['opened_boxes'] = user_opened
    
    # Получаем все открытые коробки в системе
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT DISTINCT box_id FROM opened_boxes;")
    else:
        cur.execute("SELECT DISTINCT box_id FROM opened_boxes;")
    
    all_opened = [row['box_id'] for row in cur.fetchall()]
    
    db_close(conn, cur)
    
    opened_count = len(user_opened)
    remaining = 10 - len(all_opened)
    
    return render_template('lab9/index.html',
                         login=session.get('login'),
                         opened_count=opened_count,
                         remaining=remaining,
                         gifts=gifts)

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    box_id = data.get('box_id')
    
    if box_id is None or not isinstance(box_id, int) or box_id < 0 or box_id > 9:
        return jsonify({"error": "Неверный ID коробки"}), 400
    
    conn, cur = db_connect()
    
    # Проверяем, не открыта ли уже эта коробка (в системе)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM opened_boxes WHERE box_id=%s;", (box_id,))
    else:
        cur.execute("SELECT * FROM opened_boxes WHERE box_id=?;", (box_id,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return jsonify({
            "error": "Эта коробка уже пуста! Подарок уже забрали.",
            "remaining": 10 - get_remaining_count()
        }), 400
    
    # Проверяем, не открыл ли уже пользователь 3 коробки
    user_opened = session.get('opened_boxes', [])
    if len(user_opened) >= 3:
        db_close(conn, cur)
        return jsonify({
            "error": "Вы уже открыли 3 коробки! Больше нельзя.",
            "remaining": 10 - get_remaining_count()
        }), 400
    
    # Открываем коробку - сохраняем в БД
    user_id = session.get('login', 'guest')
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO opened_boxes (box_id, user_id) VALUES (%s, %s);", 
                    (box_id, user_id))
    else:
        cur.execute("INSERT INTO opened_boxes (box_id, user_id) VALUES (?, ?);", 
                    (box_id, user_id))
    
    db_close(conn, cur)
    
    # Обновляем сессию пользователя
    user_opened.append(box_id)
    session['opened_boxes'] = user_opened
    
    # Находим данные подарка
    gift = gifts[box_id]
    
    return jsonify({
        "success": True,
        "message": gift["message"],
        "image": gift["image"],
        "opened_count": len(user_opened),
        "remaining": 10 - get_remaining_count(),
        "box_id": box_id
    })

def get_remaining_count():
    # Получить количество открытых коробок в системе
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT COUNT(DISTINCT box_id) as count FROM opened_boxes;")
    else:
        cur.execute("SELECT COUNT(DISTINCT box_id) as count FROM opened_boxes;")
    
    result = cur.fetchone()
    count = result['count'] if result else 0
    
    db_close(conn, cur)
    return count

@lab9.route('/lab9/reset_boxes', methods=['POST'])
def reset_boxes():
    if not session.get('login'):
        return jsonify({"error": "Только для авторизованных пользователей!"}), 403
    
    conn, cur = db_connect()
    
    # Очищаем таблицу opened_boxes
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM opened_boxes;")
    else:
        cur.execute("DELETE FROM opened_boxes;")
    
    db_close(conn, cur)
    
    # Очищаем сессию пользователя
    session['opened_boxes'] = []
    
    return jsonify({
        "success": True,
        "remaining": 10
    })

@lab9.route('/lab9/check_boxes')
def check_boxes():
    # Получить информацию о текущем состоянии коробок
    conn, cur = db_connect()
    
    # Все открытые коробки в системе
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT DISTINCT box_id FROM opened_boxes;")
    else:
        cur.execute("SELECT DISTINCT box_id FROM opened_boxes;")
    
    global_opened = [row['box_id'] for row in cur.fetchall()]
    
    # Коробки, открытые текущим пользователем
    user_opened = session.get('opened_boxes', [])
    
    db_close(conn, cur)
    
    return jsonify({
        "global_opened": global_opened,
        "user_opened": user_opened,
        "user_opened_count": len(user_opened),
        "global_remaining": 10 - len(global_opened)
    })

@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab9/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab9/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab9/register.html', error="Такой пользователь уже существует") 

    password_hash = generate_password_hash(password)

    # Сохранение пользователя в БД
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", 
                    (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", 
                    (login, password_hash))

    db_close(conn, cur)
    return render_template('lab9/success.html', login=login)

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab9/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab9/login.html', error="Заполните поля")

    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return render_template('lab9/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab9/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab9/success_login.html', login=login)

@lab9.route('/lab9/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab9/')