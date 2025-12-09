from flask import Blueprint, render_template, request, jsonify, abort, current_app
from datetime import datetime
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    """Создание соединения с базой данных по аналогии с lab6"""
    if current_app.config.get('DB_TYPE') == 'postgres':
        # Для PostgreSQL (если понадобится)
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='films_database',
            user='films_user',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # По умолчанию используем SQLite (как в вашем примере)
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

# ДОБАВЬ ЭТО - создаем таблицу если она не существует
def init_db():
    conn, cur = db_connect()
    
    # Создаем таблицу films если её нет
    cur.execute("""
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_ru TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    """)
    
    db_close(conn, cur)

# Вызываем создание таблицы при импорте модуля
init_db()

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films ORDER BY id")
    films = cur.fetchall()
    
    films_list = []
    for film in films:
        films_list.append(dict(film))
    
    db_close(conn, cur)
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    
    if not film:
        abort(404, description="Фильм не найден")
    
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = ?", (id,))
    db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    # Проверки
    if not film.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    if not film.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        if year < 1895 or year > 2024:
            return jsonify({'description': 'Год должен быть от 1895 до 2024'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    if not film.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    conn, cur = db_connect()
    cur.execute("""
        UPDATE films 
        SET title = ?, title_ru = ?, year = ?, description = ? 
        WHERE id = ?
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    db_close(conn, cur)
    
    return jsonify({'id': id, 'title': film['title'], 'title_ru': film['title_ru'], 'year': film['year'], 'description': film['description']})

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Проверки
    if not film.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    if not film.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        if year < 1895 or year > 2024:
            return jsonify({'description': 'Год должен быть от 1895 до 2024'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    if not film.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    conn, cur = db_connect()
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (?, ?, ?, ?)
    """, (film['title'], film['title_ru'], film['year'], film['description']))
    
    new_id = cur.lastrowid
    
    db_close(conn, cur)
    
    return jsonify({'id': new_id, 'title': film['title'], 'title_ru': film['title_ru'], 'year': film['year'], 'description': film['description']})