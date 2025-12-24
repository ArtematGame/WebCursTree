import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Удаляем старую таблицу если есть
cursor.execute("DROP TABLE IF EXISTS users")

# Создаем новую таблицу
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    phone TEXT,
    account TEXT UNIQUE,
    balance REAL DEFAULT 0,
    is_manager INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
print("Таблица users создана!")