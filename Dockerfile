# Use an official Python runtime as a parent image
FROM python:3.9-alpine

ENV MYSQL_HOST=""
ENV MYSQL_USER=""
ENV MYSQL_PASSWORD=""
ENV MYSQL_DATABASE=""

ENV REDIS_HOST=""
ENV REDIS_PORT=""
ENV REDIS_DB=""

ENV TOKEN=""

ENV XNXQDM=""
ENV PAGE_SIZE=""

ENV COOKIE=""
ENV JWXT_DOMAIN=""

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "python update_redis.py && uvicorn api:app --host 0.0.0.0 --port 8080"]
