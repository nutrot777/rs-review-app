# Multi-stage Dockerfile for RS Review Application
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose all required ports
EXPOSE 3000 8080 8081 8082 8083 8084 8085

# Start all services
CMD ["/start.sh"]