# Use a stable Python base image. 
# python:3.15.0a2 is an alpha/experimental version; 3.12 is recommended for stability.
FROM python:3.12-slim-bookworm

# Set environment variables to optimize Python performance
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required for building Python packages (like numpy/rpds-py)
# We include build-essential and others to ensure C extensions compile correctly.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first to leverage Docker layer caching
# Since you have a uv.lock file, we'll install dependencies via pip using requirements.txt
COPY requirements.txt .

# Install dependencies
# If you are using uv, you could also install uv and run 'uv pip install'
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your app runs on (adjust if necessary, e.g., 8000 for FastAPI)
EXPOSE 8000

# Use 0.0.0.0 so it's accessible outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]