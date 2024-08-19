# Use the official image as a parent image
FROM python:3.7-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP wsgi.py

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
