FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./cleanerrobot /app/cleanerrobot

CMD ["sh", "-c", "uvicorn cleanerrobot.main:app --host 0.0.0.0 --port ${APP_SERVER_PORT}"]
