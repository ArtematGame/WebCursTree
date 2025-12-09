from flask import Blueprint, render_template, request, jsonify, abort, current_app, session
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
    """Подключение к базе данных (PostgreSQL или SQLite)"""
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
    """Закрытие соединения с базой данных"""
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
    db_close(conn, cur)
    
    # Преобразуем в список словарей
    films_list = []
    for film in films:
        films_list.append(dict(film))
    
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
    
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """Удаление фильма по ID"""

    
    conn, cur = db_connect()
    
    # Проверяем существование фильма
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT id FROM films WHERE id = ?;", (id,))
        
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

    
    film_data = request.get_json()
    
    # Валидация данных
    if not film_data.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    if not film_data.get('title'):
        film_data['title'] = film_data['title_ru']
    
    if not film_data.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film_data['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    if not film_data.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film_data.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    conn, cur = db_connect()
    
    # Проверяем существование фильма
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
    else:
        cur.execute("SELECT id FROM films WHERE id = ?;", (id,))
        
    film = cur.fetchone()
    
    if not film:
        db_close(conn, cur)
        abort(404, description="Фильм не найден")
    
    # Обновляем фильм
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            UPDATE films 
            SET title = %s, title_ru = %s, year = %s, description = %s 
            WHERE id = %s
            RETURNING *;
        """, (film_data['title'], film_data['title_ru'], 
              film_data['year'], film_data['description'], id))
    else:
        cur.execute("""
            UPDATE films 
            SET title = ?, title_ru = ?, year = ?, description = ? 
            WHERE id = ?;
        """, (film_data['title'], film_data['title_ru'], 
              film_data['year'], film_data['description'], id))
        
        # Получаем обновленный фильм для SQLite
        cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
    
    updated_film = cur.fetchone()
    db_close(conn, cur)
    
    return jsonify(dict(updated_film))

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавление нового фильма"""

    film_data = request.get_json()
    
    # Валидация данных
    if not film_data.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    if not film_data.get('title'):
        film_data['title'] = film_data['title_ru']
    
    if not film_data.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film_data['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    if not film_data.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film_data.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    user_id = None
    
    conn, cur = db_connect()
    
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description, user_id) 
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        """, (film_data['title'], film_data['title_ru'], 
              film_data['year'], film_data['description'], user_id))
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description, user_id) 
            VALUES (?, ?, ?, ?, ?);
        """, (film_data['title'], film_data['title_ru'], 
              film_data['year'], film_data['description'], user_id))
        
        # Получаем ID последней вставленной записи для SQLite
        cur.execute("SELECT last_insert_rowid() as id;")
    
    new_id = cur.fetchone()['id']
    db_close(conn, cur)
    
    return jsonify({'id': new_id}), 201

@lab7.route('/lab7/rest-api/user-films/', methods=['GET'])
def get_user_films():
    """Получение фильмов текущего пользователя (если требуется авторизация)"""
    if not session.get('login'):
        abort(401, description="Требуется авторизация")
    
    conn, cur = db_connect()
    
    # Получаем ID пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (session['login'],))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (session['login'],))
        
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        abort(404, description="Пользователь не найден")
    
    # Получаем фильмы пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM films WHERE user_id = %s ORDER BY id;", (user['id'],))
    else:
        cur.execute("SELECT * FROM films WHERE user_id = ? ORDER BY id;", (user['id'],))
        
    films = cur.fetchall()
    db_close(conn, cur)
    
    # Преобразуем в список словарей
    films_list = []
    for film in films:
        films_list.append(dict(film))
    
    return jsonify(films_list)