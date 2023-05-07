# Встановлюємо залежності
FROM python:3.11
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

# Копіюємо файли додатку в контейнер
COPY web_app.py /app/web_app.py
COPY index.html /app/index.html
COPY message.html /app/message.html
COPY style.css /app/style.css
COPY logo.png /app/logo.png
COPY error.html /app/error.html

# Встановлюємо каталог робочої директорії
WORKDIR /app

# Перевіряємо існування каталогу storage та файлу data.json
RUN mkdir -p storage
RUN touch storage/data.json

# Запускаємо додаток
CMD python web_app.py
