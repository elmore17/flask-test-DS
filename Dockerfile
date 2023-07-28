# Используем базовый образ Python
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта
COPY requirements.txt /app/

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Копируем все содержимое текущей директории внутрь контейнера
COPY . /app/

# Задаем переменную окружения для Flask (необязательно)
ENV FLASK_APP=app.py

# Открываем порт, на котором будет работать приложение
EXPOSE 5000

# Запускаем приложение при старте контейнера
CMD ["flask", "run", "--host=0.0.0.0"]
