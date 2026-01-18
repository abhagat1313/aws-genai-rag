# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app


# Install dependencies
COPY src/ src/
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
