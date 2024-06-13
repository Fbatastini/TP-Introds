# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory
COPY . .

# Expose the port for the API
EXPOSE 5001

# Set the command to run the API
ENV FLASK_APP=api.py
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]