FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Expose API port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV AGENT_API_HOST=0.0.0.0
ENV AGENT_API_PORT=5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run the API server
CMD ["python", "api_server.py"]
