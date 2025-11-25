from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

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

def get_offices_from_db():
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
    else:
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
    
    offices_data = cur.fetchall()
    db_close(conn, cur)
    
    offices = []
    for office in offices_data:
        offices.append({
            "number": office['number'],
            "tenant": office['tenant'] or "",
            "price": office['price']
        })
    
    return offices

def update_office_in_db(office_number, tenant):
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE offices SET tenant = %s WHERE number = %s;",
            (tenant, office_number)
        )
    else:
        cur.execute(
            "UPDATE offices SET tenant = ? WHERE number = ?;",
            (tenant, office_number)
        )
    
    db_close(conn, cur)

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html', login=session.get('login')) 

@lab6.route('/lab6/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab6/')

@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        offices = get_offices_from_db()
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        offices = get_offices_from_db()
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id    
                    }
                
                update_office_in_db(office_number, login)
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    if data['method'] == 'cancellation':
        office_number = data['params']
        offices = get_offices_from_db()
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == '':
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel another user\'s booking'
                        },
                        'id': id
                    }
                
                update_office_in_db(office_number, "")
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }