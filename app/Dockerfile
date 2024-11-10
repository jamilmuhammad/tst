FROM python:3.11-slim

WORKDIR /code

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY ./app /code/app

# Set environment variables
ENV DATABASE_URL = postgresql://user:pass@localhost:5432/library_db
ENV REDIS_URL = redis://localhost:6379

ENV PYTHONPATH=/code
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]