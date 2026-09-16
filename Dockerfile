FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY server.py .
COPY indian_stocks.py .
COPY crypto_commodities.py .
COPY portfolio_tracker.py .
COPY powerbi_integration.py .
COPY powerbi_api.py .
COPY dashboard/ ./dashboard/

# Create directory for data persistence
RUN mkdir -p /app/data

# Expose ports
EXPOSE 8050 8000 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Run the application
CMD ["gunicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}", "--workers", "4", "--timeout", "120"]