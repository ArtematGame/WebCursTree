from flask import Blueprint, render_template, request, jsonify, abort, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

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

    return conn, cur  # Возвращаем ДВА значения!

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html') 

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()  # Получаем ДВА значения!
    cur.execute("SELECT * FROM films")
    films = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)  # Используем правильную функцию закрытия
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()  # Получаем ДВА значения!
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    
    film = cur.fetchone()
    db_close(conn, cur)  # Используем правильную функцию закрытия
    
    if not film:
        abort(404, description="Фильм не найден")
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()  # Получаем ДВА значения!
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ?", (id,))
    
    db_close(conn, cur)  # Используем правильную функцию закрытия
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    # Проверка русского названия
    if not film.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    # Если оригинальное пустое - копируем русское
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    # Проверка года
    if not film.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    # Проверка описания
    if not film.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    conn, cur = db_connect()  # Получаем ДВА значения!
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE films 
            SET title = %s, title_ru = %s, year = %s, description = %s
            WHERE id = %s
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    else:
        cur.execute("""
            UPDATE films 
            SET title = ?, title_ru = ?, year = ?, description = ?
            WHERE id = ?
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    
    db_close(conn, cur)  # Используем правильную функцию закрытия
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    # Проверка русского названия
    if not film.get('title_ru'):
        return jsonify({'description': 'Заполните русское название'}), 400
    
    # Если оригинальное пустое - копируем русское
    if not film.get('title'):
        film['title'] = film['title_ru']
    
    # Проверка года
    if not film.get('year'):
        return jsonify({'description': 'Укажите год'}), 400
    
    try:
        year = int(film['year'])
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'description': f'Год должен быть от 1895 до {current_year}'}), 400
    except ValueError:
        return jsonify({'description': 'Год должен быть числом'}), 400
    
    # Проверка описания
    if not film.get('description'):
        return jsonify({'description': 'Заполните описание'}), 400
    
    if len(film.get('description', '')) > 2000:
        return jsonify({'description': 'Описание должно быть не более 2000 символов'}), 400
    
    conn, cur = db_connect()  # Получаем ДВА значения!
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s)
        """, (film['title'], film['title_ru'], film['year'], film['description']))
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?)
        """, (film['title'], film['title_ru'], film['year'], film['description']))
    
    film_id = cur.lastrowid
    db_close(conn, cur)  # Используем правильную функцию закрытия
    
    result_film = {
        'id': film_id,
        'title': film['title'],
        'title_ru': film['title_ru'],
        'year': film['year'],
        'description': film['description']
    }
    return jsonify(result_film)