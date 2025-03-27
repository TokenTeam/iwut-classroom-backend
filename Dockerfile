# Use an official Python runtime as a parent image
FROM python:3.9-slim

ARG _MYSQL_HOST
ARG _MYSQL_USER
ARG _MYSQL_PASSWORD
ARG _MYSQL_DATABASE

ARG _REDIS_HOST 
ARG _REDIS_PORT 
ARG _REDIS_DB

ARG _TOKEN

ARG _XNXQDM 
# 学年学期代码 
# example '2024-2025-2'

ARG _PAGE_SIZE
# 爬取的教室数

# Define environment variables for database configuration
ENV MYSQL_HOST = ${_MYSQL_HOST}
ENV MYSQL_USER = ${_MYSQL_USER}
ENV MYSQL_PASSWORD = ${_MYSQL_PASSWORD}
ENV MYSQL_DATABASE = ${_MYSQL_DATABASE}

ENV REDIS_HOST = ${_REDIS_HOST}
ENV REDIS_PORT = ${_REDIS_PORT}
ENV REDIS_DB = ${_REDIS_DB}

ENV TOKEN = ${_TOKEN}

ENV XNXQDM = ${_XNXQDM}
ENV PAGE_SIZE = ${_PAGE_SIZE}

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80



# Define other environment variables
ENV NAME World

# # Run app.py when the container launches
# CMD ["python", "app.py"]

# 设置 FastAPI 启动命令
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
