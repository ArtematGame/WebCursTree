def get_db():
    """Получает соединение с базой данных"""
    import os
    
    # Правильный путь к базе в sqlite3 папке
    db_path = '/home/Artemat/WebCursTree/sqlite3/database.db'
    
    print(f"ПОДКЛЮЧАЕМСЯ К БАЗЕ: {db_path}")
    print(f"ФАЙЛ СУЩЕСТВУЕТ: {os.path.exists(db_path)}")
    
    if not os.path.exists(db_path):
        print(f"ОШИБКА: База не найдена! Создаем...")
        # Создаем папку если её нет
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # Создаем новую базу с таблицей
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
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
    else:
        conn = sqlite3.connect(db_path)
    
    conn.row_factory = sqlite3.Row
    
    # Проверяем что таблица существует
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("ОШИБКА: Таблица users не найдена в базе!")
            # Создаем таблицу
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
            print("Таблица users создана")
    except Exception as e:
        print(f"ОШИБКА ПРОВЕРКИ: {e}")
    
    return conn