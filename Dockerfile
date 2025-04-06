FROM python:3.11-slim

# Set environment variables
ENV APP_HOME=/app
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=$APP_HOME/src  

# Set the working directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependencies
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry install --no-root

# Copy the rest of the application code into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]