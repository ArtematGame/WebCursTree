from flask import Blueprint, render_template, request, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

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

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует") 

    password_hash = generate_password_hash(password)

    #Сохранение пользователя в БД
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", 
                    (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", 
                    (login, password_hash, real_name))

    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    
    #Получение найденной записи
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = True if request.form.get('is_favorite') else False
    is_public = True if request.form.get('is_public') else False

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните название и текст статьи')
 
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);", 
                    (user_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);", 
                    (user_id, title, article_text, is_favorite, is_public))

    db_close(conn, cur)
    return redirect('/lab5/')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        
    user_row = cur.fetchone()
    user_id = user_row[0]

    # Исправляем сортировку - сначала избранные, потом остальные
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC NULLS LAST, id DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC, id DESC;", (user_id,))
        
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    
    # Ищем статьи где is_public = TRUE
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE is_public = true;")
    else:
        cur.execute("SELECT * FROM articles WHERE is_public = 1;")
        
    articles = cur.fetchall()
    
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    # Находим ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        
    user_id = cur.fetchone()["id"]

    # Удаляем статью этого пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if not session.get('login'):
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        # Показываем форму редактирования
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
        article = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    # Сохраняем изменения
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", 
                    (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", 
                    (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def all_users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users;")
    else:
        cur.execute("SELECT login, real_name FROM users;")
        
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        # Получаем текущие данные пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT real_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    # Обработка формы
    new_real_name = request.form.get('real_name')
    new_password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Проверка подтверждения пароля
    if new_password and new_password != confirm_password:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user={'real_name': new_real_name}, error='Пароли не совпадают')

    # Обновляем данные
    if new_password:
        # Меняем имя и пароль
        password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s, password=%s WHERE login=%s;", 
                        (new_real_name, password_hash, login))
        else:
            cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;", 
                        (new_real_name, password_hash, login))
    else:
        # Меняем только имя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (new_real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?;", (new_real_name, login))

    db_close(conn, cur)
    return redirect('/lab5/')

