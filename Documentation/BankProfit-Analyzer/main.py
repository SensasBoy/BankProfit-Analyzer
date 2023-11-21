import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import *
from tkinter import messagebox, ttk, simpledialog
import sys

# Подключение к базе данных SQLite
conn = sqlite3.connect('bank_data.db')
cursor = conn.cursor()
# Создание таблицы, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS deposits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        interest_rate REAL,
        duration INTEGER,
        profit REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS total_amount (
        id INTEGER PRIMARY KEY,
        amount REAL
    )
''')
conn.commit()
# Создание таблицы для хранения общей суммы вложенных денег
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', '1111')")
conn.commit()


def authenticate():

    username = simpledialog.askstring("Аутентификация", "Введите логин:", parent=root)
    password = simpledialog.askstring("Аутентификация", "Введите пароль:", parent=root)

    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user_data = cursor.fetchone()

    if user_data:
        return True
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")
        return False


def exit_program():
    result = messagebox.askquestion("Выход", "Вы уверены, что хотите выйти из программы?")
    if result == "yes":
        conn.close()
        root.destroy()
        sys.exit()


def calculate_profit(amount, interest_rate, duration):
    # Расчет прибыли от вклада
    profit = amount * (interest_rate / 100) * duration
    return profit


def validate_input(amount_entry, interest_rate_entry, duration_entry):
    try:
        amount = float(amount_entry.get())
        interest_rate = float(interest_rate_entry.get())
        duration = int(duration_entry.get())

        # Дополнительные проверки
        if amount <= 0 or interest_rate < 0 or duration <= 0:
            raise ValueError("Некорректные значения")

        return True
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректно введенные данные. Пожалуйста, введите корректные числовые значения. ({str(e)})")
        return False
    except Exception:
        return False

def update_total_amount():
    # Обновление общей суммы вложенных денег
    cursor.execute('SELECT SUM(amount) FROM deposits')
    total_amount = cursor.fetchone()[0]
    if total_amount is None:
        total_amount = 0.0

    # Обновление суммы в таблице total_amount
    cursor.execute('INSERT OR REPLACE INTO total_amount (id, amount) VALUES (1, ?)', (total_amount,))
    conn.commit()

    # Обновление текста метки
    total_amount_label.config(text=f"Сумма вложенных денег: {total_amount:.2f} руб.")


def save_deposit(amount, interest_rate, duration):
    if validate_input(amount_entry, interest_rate_entry, duration_entry):
        # Сохранение данных о вкладе в базу данных
        profit = calculate_profit(amount, interest_rate, duration)
        cursor.execute('''
            INSERT INTO deposits (amount, interest_rate, duration, profit)
            VALUES (?, ?, ?, ?)
        ''', (amount, interest_rate, duration, profit))
        conn.commit()

        # Обновление суммы вложенных денег
        update_total_amount()
    else:
        messagebox.showerror("Ошибка", "Некорректные данные. Пожалуйста, исправьте ввод.")


def plot_deposits():
    # Получение данных из базы данных
    cursor.execute('SELECT id, profit FROM deposits')
    data = cursor.fetchall()

    # Создание DataFrame из данных
    df = pd.DataFrame(data, columns=['id', 'profit'])

    # Проверка на минимальные значения для отображения графика
    min_profit = 1  # Минимальная прибыль для отображения графика
    if df['profit'].sum() < min_profit:
        messagebox.showinfo("Недостаточно данных", "Недостаточно данных для построения графика.")
        return

    # Строим график
    plt.plot(df['id'], df['profit'], label='Прибыль')
    plt.xlabel('ID вклада')
    plt.ylabel('Прибыль')
    plt.title('Прибыль от вкладов во времени')
    plt.legend()
    plt.show()

    # Выводим таблицу с прибылью
    print(df)
    print_total_profit()


def print_total_profit():
    # Получение общей прибыли из базы данных
    cursor.execute('SELECT SUM(profit) FROM deposits')
    total_profit = cursor.fetchone()[0]

    # Обновляем текст метки с общей прибылью
    total_profit_label.config(text=f"Общая прибыль: {total_profit:.2f} руб.")


def initialize_total_amount():
    # Получение последней сохраненной суммы вложенных денег из базы данных
    cursor.execute('SELECT amount FROM total_amount')
    last_total_amount = cursor.fetchone()

    # Вызов функции для инициализации суммы вложенных денег
    if last_total_amount:
        update_total_amount(last_total_amount[0])
    else:
        update_total_amount(0.0)


def reset_table():
    # Сброс всей таблицы
    cursor.execute('DROP TABLE IF EXISTS deposits')
    cursor.execute('DROP TABLE IF EXISTS total_amount')  #
    cursor.execute('''
        CREATE TABLE deposits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            interest_rate REAL,
            duration INTEGER,
            profit REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE total_amount (
            id INTEGER PRIMARY KEY,
            amount REAL
        )
    ''')
    conn.commit()
    messagebox.showinfo("Сброс таблицы", "Таблица сброшена.")
    # Обновление текста метки
    total_amount_label.config(text="Сумма вложенных денег: 0.0 руб.")
    total_profit_label.config(text="Общая прибыль: 0.0 руб.")



root = Tk()
root.withdraw()

if authenticate():
    # Создание основного окна приложения
    print("Пользователь успешно аутентифицирован")
    root = Tk()
    root.title("Калькулятор вкладов")
    root.geometry("400x400")
    amount_label = Label(root, text="Сумма вклада:")
    amount_entry = Entry(root)

    interest_rate_label = Label(root, text="Процентная ставка (%):")
    interest_rate_entry = Entry(root)

    duration_label = Label(root, text="Срок вклада (лет):")
    duration_entry = Entry(root)

    save_button = Button(root, text="Сохранить вклад", command=lambda: save_deposit(
        float(amount_entry.get()),
        float(interest_rate_entry.get()),
        int(duration_entry.get())
    ))

    plot_button = Button(root, text="График вкладов", command=plot_deposits)

    reset_button = Button(root, text="Сброс таблицы", command=reset_table)

    # Метка для отображения общей прибыли
    total_profit_label = Label(root, text="Общая прибыль: 0.0 руб.")
    total_profit_label.grid(row=8, column=0, columnspan=2, pady=10)

    # Метка для отображения суммы вложенных денег
    total_amount_label = Label(root, text="Сумма вложенных денег: 0.0 руб.")
    total_amount_label.grid(row=9, column=0, columnspan=2, pady=20)

    # Вызов функции для обновления суммы вложенных денег
    update_total_amount()

    currency_label = Label(root, text="Выберите валюту:")
    currency_values = ["USD", "RUB", "EUR"]
    currency = ttk.Combobox(root, values=currency_values, state="readonly")
    currency.set("RUB")  # Установите начальное значение валюты
    currency_label.grid(row=3, column=0, pady=5)
    currency.grid(row=3, column=1, pady=5)

    # Добавление кнопки выхода из программы
    exit_button = Button(root, text="Выход", command=exit_program)
    exit_button.grid(row=10, column=0, columnspan=2, pady=10)

    # Размещение элементов интерфейса на сетке
    amount_label.grid(row=0, column=0, padx=5, pady=5)
    amount_entry.grid(row=0, column=1, padx=5, pady=5)

    interest_rate_label.grid(row=1, column=0, padx=5, pady=5)
    interest_rate_entry.grid(row=1, column=1, padx=5, pady=5)

    duration_label.grid(row=2, column=0, padx=5, pady=5)
    duration_entry.grid(row=2, column=1, padx=5, pady=5)

    save_button.grid(row=5, column=0, columnspan=2, pady=10)
    plot_button.grid(row=6, column=0, columnspan=2, pady=10)
    reset_button.grid(row=7, column=0, columnspan=2, pady=10)

    # Метка для общей прибыли
    total_profit_label = Label(root, text="Общая прибыль: 0.0 руб.")
    total_profit_label.grid(row=8, column=0, columnspan=2, pady=10)

    initialize_total_amount

    # Запуск основного цикла обработки событий
    root.mainloop()
else:
    messagebox.showerror("Ошибка", "Неверный логин или пароль")
    print("Аутентификация не удалась")

# Закрытие соединения с базой данных
conn.close()
