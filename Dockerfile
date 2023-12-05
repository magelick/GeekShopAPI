# Версия образа, на основе которого будет создан контейнер
FROM python:3.11.6-alpine3.18

# Создаём рабочую папку внутри контейнера
WORKDIR /app

# Копируем все файлы в рабочую папку
COPY . /app

# Устанавливаем все зависимости в рабочей папке
RUN  pip install --no-cache-dir -r /app/requirements.txt

# Указываем Python не создавать кэш файлы с байт кодом рус
ENV PYTHONDONTWRITEBYTECODE 1
# Указываем Python что нет необходимости кэшировать ввод/вывод
ENV PYTHONUNBUFFERED 1

# Просим открыть на 8000 порту контейнер
EXPOSE 8000