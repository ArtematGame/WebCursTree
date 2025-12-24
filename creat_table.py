import sqlite3

# Используем тот же путь что и в rgz.py
db_path = '/home/Artemat/WebCursTree/sqlite3/database.db'

conn = sqlite3.connect(db_path)
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
print(f"Таблица users создана в {db_path}!")