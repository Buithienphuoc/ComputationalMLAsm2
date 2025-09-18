# Base image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run migrations + load CSV + start server
CMD python manage.py migrate && \
    python manage.py import_teams_players && \
    gunicorn ai_project.wsgi:application --bind 0.0.0.0:$PORT
