# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NLTK_DATA=/app/nltk_data

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with specific handling for pytablericons
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --force-reinstall pytablericons==1.0.1
RUN pip install --no-cache-dir -r requirements.txt

# Verify pytablericons installation
RUN python -c "import pytablericons; print('pytablericons installed successfully')"

# Create NLTK data directory
RUN mkdir -p /app/nltk_data

# Copy application code
COPY . .

# Create .streamlit directory and copy config
RUN mkdir -p .streamlit
COPY .streamlit/config.toml .streamlit/config.toml

# Expose port
EXPOSE $PORT

# Health check
HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health

# Run the application
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
