from flask import Blueprint, render_template, request, jsonify, abort, session, current_app
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

def db_connect():
    """Подключение к БД в зависимости от конфигурации"""
    if current_app.config.get('DB_TYPE') == 'postgres':
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
    """Закрытие соединения с БД"""
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """Получение всех фильмов"""
    conn, cur = db_connect()
    
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM films ORDER BY id;")
    else:
        cur.execute("SELECT * FROM films ORDER BY id;")
    
    films = cur.fetchall()
    
    # Конвертируем результат в список словарей
    films_list = []
    for film in films:
        if isinstance(film, dict):
            films_list.append(film)
        else:
            films_list.append(dict(film))
    
    db_close(conn, cur)
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    """Получение конкретного фильма по ID"""
    conn, cur = db_connect()
    
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
    
    film = cur.fetchone()
    db_close(conn, cur)
    
    if not film:
        abort(404, description="Фильм не найден")
    
    # Конвертируем в словарь
    if not isinstance(film, dict):
        film = dict(film)
    
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """Удаление фильма по ID"""
    # Проверяем авторизацию
    login = session.get('login')
    if not login:
        return jsonify({'description': 'Требуется авторизация'}), 401
    
    conn, cur = db_connect()
    
    # Проверяем существование фильма
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
    
    film = cur.fetchone()
    
    if not film:
        db_close(conn, cur)
        abort(404, description="Фильм не найден")
    
    # Удаляем фильм
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ?;", (id,))
    
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Обновление фильма по ID"""
    # Проверяем авторизацию
    login = session.get('login')
    if not login:
        return jsonify({'description': 'Требуется авторизация'}), 401
    
    conn, cur = db_connect()
    
    # Проверяем существование фильма
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
    
    if not cur.fetchone():
        db_close(conn, cur)
        abort(404, description="Фильм не найден")
    
    film = request.get_json()
    
    # Валидация данных
    if not film.get('title_ru'):
        db_close(conn, cur)
        return jsonify({'description': 'Заполните русское название'}), 400
    
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    if not film.get('year'):
        db_close(conn, cur)
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            db_close(conn, cur)
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        db_close(conn, cur)
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    if not film.get('description'):
        db_close(conn, cur)
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        db_close(conn, cur)
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    # Получаем ID пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
    
    user = cur.fetchone()
    user_id = user['id'] if user else None
    
    # Обновляем фильм
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            UPDATE films 
            SET title = %s, title_ru = %s, year = %s, description = %s, user_id = %s 
            WHERE id = %s;
        """, (film['title'], film['title_ru'], film['year'], film['description'], user_id, id))
    else:
        cur.execute("""
            UPDATE films 
            SET title = ?, title_ru = ?, year = ?, description = ?, user_id = ? 
            WHERE id = ?;
        """, (film['title'], film['title_ru'], film['year'], film['description'], user_id, id))
    
    db_close(conn, cur)
    
    # Возвращаем обновленный фильм
    return get_film(id)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавление нового фильма"""
    # Проверяем авторизацию
    login = session.get('login')
    if not login:
        return jsonify({'description': 'Требуется авторизация'}), 401
    
    conn, cur = db_connect()
    
    film = request.get_json()
    
    # Валидация данных
    if not film.get('title_ru'):
        db_close(conn, cur)
        return jsonify({'description': 'Заполните русское название'}), 400
    
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    if not film.get('year'):
        db_close(conn, cur)
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            db_close(conn, cur)
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        db_close(conn, cur)
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    if not film.get('description'):
        db_close(conn, cur)
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        db_close(conn, cur)
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    # Получаем ID пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
    
    user = cur.fetchone()
    user_id = user['id'] if user else None
    
    # Добавляем фильм в БД
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description, user_id) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (film['title'], film['title_ru'], film['year'], film['description'], user_id))
        
        new_id = cur.fetchone()['id']
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description, user_id) 
            VALUES (?, ?, ?, ?, ?);
        """, (film['title'], film['title_ru'], film['year'], film['description'], user_id))
        
        new_id = cur.lastrowid
    
    db_close(conn, cur)
    
    # Возвращаем ID нового фильма
    return jsonify({'id': new_id}), 201

@lab7.route('/lab7/rest-api/films/user/<login>', methods=['GET'])
def get_user_films(login):
    """Получение фильмов, добавленных конкретным пользователем"""
    conn, cur = db_connect()
    
    # Получаем ID пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
    
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return jsonify([])
    
    user_id = user['id']
    
    # Получаем фильмы пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM films WHERE user_id = %s ORDER BY id;", (user_id,))
    else:
        cur.execute("SELECT * FROM films WHERE user_id = ? ORDER BY id;", (user_id,))
    
    films = cur.fetchall()
    
    # Конвертируем результат в список словарей
    films_list = []
    for film in films:
        if isinstance(film, dict):
            films_list.append(film)
        else:
            films_list.append(dict(film))
    
    db_close(conn, cur)
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/my', methods=['GET'])
def get_my_films():
    """Получение фильмов текущего пользователя"""
    login = session.get('login')
    if not login:
        return jsonify({'description': 'Требуется авторизация'}), 401
    
    return get_user_films(login)