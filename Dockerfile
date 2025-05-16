# Dockerfile

# 1. Base Image: Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set Work Directory: Create and set the working directory in the container
WORKDIR /app

# 4. Install System Dependencies (if any, e.g., for Pillow or database drivers)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     # Example: libpq-dev gcc for psycopg2 if you were using PostgreSQL
#     # Add other system dependencies here if needed
#     && rm -rf /var/lib/apt/lists/*

# 5. Install Python Dependencies
# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code: Copy the rest of your application code into the container
COPY . .

# 7. Collect Static Files (Good practice, though runserver handles it in DEBUG mode)
# Ensure your darshanam_dev.settings has STATIC_ROOT configured
# e.g., STATIC_ROOT = BASE_DIR / 'staticfiles'
# RUN python manage.py collectstatic --noinput

# 8. Expose Port: Make port 8111 available to the outside world
EXPOSE 8111

# 9. Command to Run: The command to run your application
# Using 0.0.0.0 makes the server accessible from outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8111"]