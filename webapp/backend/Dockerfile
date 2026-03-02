FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/app/
COPY run.py .

# Disable Python output buffering so logs reach Docker immediately
ENV PYTHONUNBUFFERED=1

ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

EXPOSE 5000

# 1 worker + 4 threads: handles concurrent SSE streams without blocking other requests
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "300", "run:app"]
