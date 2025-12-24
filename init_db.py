# Файл: init_db.py
import sqlite3
import hashlib

def init_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Проверяем, есть ли уже пользователи
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    if user_count > 0:
        print(f"В базе уже есть {user_count} пользователей. Пропускаем инициализацию.")
        conn.close()
        return
    
    # Данные для вставки
    users_to_insert = [
        # (id, login, password, real_name, phone, account, balance, is_manager)
        (1, 'admin', 'admin123', 'Иванов Иван', '+79001112233', 'ADMIN001', 0, True),
        (2, 'client1', 'client123', 'Сидорова Анна', '+79003334455', 'ACC001', 1000, False),
        (3, 'client2', 'client123', 'Кузнецов Сергей', '+79004445566', 'ACC002', 1000, False),
        (4, 'client3', 'client123', 'Смирнова Ольга', '+79005556677', 'ACC003', 1000, False),
        (5, 'client4', 'client123', 'Васильев Дмитрий', '+79006667788', 'ACC004', 1000, False),
        (6, 'client5', 'client123', 'Николаева Елена', '+79007778899', 'ACC005', 1000, False),
        (7, 'client6', 'client123', 'Алексеев Алексей', '+79008889900', 'ACC006', 1000, False),
        (8, 'client7', 'client123', 'Павлова Мария', '+79009990011', 'ACC007', 1000, False),
        (9, 'client8', 'client123', 'Федоров Андрей', '+79001001122', 'ACC008', 1000, False),
        (10, 'client9', 'client123', 'Соколова Виктория', '+79001112233', 'ACC009', 1000, False),
        (11, 'client10', 'client123', 'Лебедев Максим', '+79001223344', 'ACC010', 1000, False),
    ]

    
    print("Начинаем заполнение базы данных...")
    
    for user_data in users_to_insert:
        user_id, login, password, real_name, phone, account, balance, is_manager = user_data
        
        # Хешируем пароль
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:

            cursor.execute(
                "INSERT INTO users (id, login, password, real_name, phone, account  balance, is_manager) VALUES (?, ?, ?, ?)",
                (user_id, login, password_hash, real_name, phone, account, balance, is_manager)
            )
        
            
            print(f"Добавлен пользователь: {login}")
            
        except Exception as e:
            print(f"Ошибка при добавлении {login}: {e}")
            conn.rollback()
            conn.close()
            return
    
    conn.commit()
    conn.close()
    print(f"База данных инициализирована! Добавлено {len(users_to_insert)} пользователей.")

def check_database():
    """Проверяем состояние базы данных"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    print("\n=== Проверка базы данных ===")
    
    # Проверяем таблицу users
    try:
        cursor.execute("SELECT COUNT(*) as count, 'users' as table_name FROM users")
        result = cursor.fetchone()
        print(f"Таблица users: {result[0]} записей")
    except Exception as e:
        print(f"Ошибка при проверке таблицы users: {e}")
    
    
    conn.close()

if __name__ == '__main__':
    # Сначала проверяем
    check_database()
    
    # Спрашиваем, нужно ли заполнять
    response = input("\nЗаполнить базу данных тестовыми пользователями? (y/n): ")
    if response.lower() == 'y':
        init_database()
        print("\nПосле инициализации:")
        check_database()
    else:
        print("Заполнение отменено.")