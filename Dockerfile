# Dockerfile for HealthStack-System Django app
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-mysql-client \
    default-libmysqlclient-dev \
    pkg-config \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Add wait-for-it script
# COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

EXPOSE 8000

# Wait for MySQL before starting backend
# CMD ["/wait-for-it.sh", "db:3306", "--", "npm", "start"]

# Run migrations and start server
CMD ["/wait-for-it.sh", "db:3306", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
