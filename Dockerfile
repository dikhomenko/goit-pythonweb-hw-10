FROM python:3.12p
ENV APP_HOME /app
WORKDIR ${APP_HOME}

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code into the container
COPY . .

# Define the volume for the storage directory
VOLUME ["/app/storage"]

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "python", "src/app/main.py"]