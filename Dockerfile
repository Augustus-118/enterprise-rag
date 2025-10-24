# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose port (Render uses PORT env variable)
EXPOSE 8000

# Run the application
# Use shell form to allow environment variable expansion
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}
