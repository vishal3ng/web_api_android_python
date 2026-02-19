FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy framework files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HEADLESS=true

# Default command
CMD ["pytest", "--browser=chromium", "--headed=false"]
