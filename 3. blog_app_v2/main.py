from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import json


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.context_processor
def inject_constants():
    return {
        'HOME_URL': url_for('index'),
        'SITE_NAME': '["Блог программиста"]',
        'CURRENT_YEAR': 2026
    }


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route("/notes")
def notes():
    try:
        # Читаем данные из JSON-файла
        with open('notes.json', 'r', encoding='utf-8') as file:
            notes_data = json.load(file)
    except FileNotFoundError:
        # Если файла нет, создаём пустой словарь
        notes_data = {}
    except json.JSONDecodeError:
        # Если файл есть, но содержит некорректный JSON
        notes_data = {}

    # Передаём данные в шаблон
    return render_template("notes.html", notes=notes_data)


@app.route("/submit", methods=["POST"])
def submit():
    caption = request.form["caption"]
    message = request.form["message"]

    if not caption or not message:
        return "Ошибка: все поля обязательны для заполнения", 400

    # Получаем текущую дату и время в читаемом формате
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    # Формируем ключ: заголовок + временная метка
    key = f"{caption} ({timestamp})"

    # Создаём словарь с данными
    note_data = {key: message}

    try:
        # Читаем существующие данные из JSON‑файла, если он есть
        try:
            with open('notes.json', 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            # Если файла нет, создаём пустой словарь
            existing_data = {}

        # Обновляем существующие данные новыми
        existing_data.update(note_data)

        # Записываем обновлённые данные обратно в файл
        with open('notes.json', 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    except Exception as e:
        # Обрабатываем возможные ошибки при работе с файлом
        return f"Ошибка при сохранении данных: {str(e)}", 500

    # Перенаправляем пользователя на страницу с заметками
    return redirect(url_for('notes'))


if __name__ == "__main__":
    app.run(debug=True)
