import flet as ft
import sqlite3
import time

# Функция для получения сообщений из базы данных
def get_messages():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT user, message FROM messages ORDER BY timestamp DESC')
    messages = c.fetchall()
    conn.close()
    return messages

# Функция для отправки нового сообщения
def send_message(message):
    # Здесь отправляем сообщение в Telegram через API
    print(f"Отправлено сообщение: {message}")
    # Пример: requests.post(f'https://api.telegram.org/bot{YOUR_TOKEN}/sendMessage', data={"text": message})

# Основной интерфейс Flet
def main(page: ft.Page):
    page.title = "Чат с Telegram-ботом"
    page.vertical_alignment = ft.MainAxisAlignment.START

    messages_list = ft.Column(scroll="adaptive")

    # Отображаем старые сообщения
    def update_chat():
        messages_list.controls.clear()
        for msg in get_messages():
            messages_list.controls.append(ft.Text(f"{msg[0]}: {msg[1]}"))
        page.update()

    # Функция для обработки нового сообщения
    def on_send_click(e):
        message = message_input.value
        if message:
            send_message(message)
            message_input.value = ""
            update_chat()

    # Компоненты интерфейса
    message_input = ft.TextField(label="Введите сообщение", autofocus=True)
    send_button = ft.ElevatedButton("Отправить", on_click=on_send_click)

    page.add(messages_list, message_input, send_button)

    # Обновляем чат каждую секунду
    while True:
        update_chat()
        time.sleep(1)

# Запуск приложения Flet
ft.app(target=main)
