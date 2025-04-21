FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=app.py  

COPY . .


CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]