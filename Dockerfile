#Dockerfile

# Дата создания: 16.11.2023 5:48 (мск)
# Статус: запущен и проверен
# Назначение: Хакатон, решение кейса г. Москва
# Права на содержимое: Siplusplusov (KIRISHIKI TEAM)

# Для использования:
# 1. Установить движок Docker на устройство
# 2. Собрать контейнер командой docker build -t gundet-shiki  .
# 3. Запустить командой docker run -p 8501:8501 gundet-shiki

FROM python:3.11.5

# создание директории проекта
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN apt update
RUN apt install -y libgl1-mesa-dev
RUN pip install opencv-python==4.6.0.66
RUN pip install --upgrade ultralytics

# назначение порта для проброски
EXPOSE 8501

# выполнение проверки localhost
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# запуск контейнера в изолированной среде
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]