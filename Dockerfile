FROM python:3.10.14-bullseye

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Создаем виртуальное окружение, активируем его и устанавливаем зависимости
# RUN python -m venv env && \
#     /app/env/bin/pip install --upgrade pip && \
#     /app/env/bin/pip install -r requirements.txt --no-cache-dir
RUN pip install -r requirements.txt

# Копируем все файлы проекта в рабочую директорию контейнера
COPY . .

# Устанавливаем переменные окружения для использования виртуального окружения
# ENV PATH="/app/env/bin:$PATH"
# ENV VIRTUAL_ENV="/app/env"

# Указываем команду для запуска приложения
#CMD ["sh", "/app/entrypoint.sh"]
CMD [sh, /app/entrypoint.sh]


# # Use an official Python runtime as a parent image
# FROM python:3.10-slim
#
# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
#
# # Create a non-root user and group
# RUN groupadd -r -g 999 django && useradd -r -u 999 -g django django
#
# # Set working directory
# WORKDIR /app
#
# # Install netcat and apt-utils
# RUN apt-get update && apt-get install -y netcat-traditional apt-utils && apt-get clean
#
# # Copy requirements.txt
# COPY requirements.txt /app/
#
# # Install dependencies
# RUN pip install --upgrade pip && pip install -r requirements.txt
#
# # Copy project files
# COPY . /app/
#
# # Add entrypoint.sh, change its permissions and ownership
# COPY ./entrypoint.sh /app/entrypoint.sh
# RUN chmod +x /app/entrypoint.sh
# RUN chown 999:999 /app/entrypoint.sh
#
# # Change ownership of /app
# RUN chown -R 999:999 /app
#
#
# # Create and set permissions for debug.log
# RUN touch /app/debug.log && chmod 666 /app/debug.log
# RUN chown django:django /app/debug.log
#
#
#
# # Switch to the new user
# USER django
#
# # Expose port
# EXPOSE 8000
#
# # Run entrypoint.sh
# ENTRYPOINT ["/app/entrypoint.sh"]
