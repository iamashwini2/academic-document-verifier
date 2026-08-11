FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (Tesseract, poppler for PDF rendering if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       tesseract-ocr \
       poppler-utils \
       libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure Tesseract path env for the app
ENV TESSERACT_PATH=/usr/bin/tesseract

# Default port (Render provides $PORT at runtime)
ENV PORT=5000

# Run with Gunicorn; allow overriding PORT at runtime
CMD ["sh", "-c", "gunicorn backend.app:app -b 0.0.0.0:${PORT} --workers 1"]
