import sqlite3

# Подключаемся к той же базе
conn = sqlite3.connect('/home/Artemat/WebCursTree/sqlite3/database.db')
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_account TEXT,
        to_account TEXT,
        amount REAL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

print("Таблица 'transactions' создана!")
conn.commit()
conn.close()