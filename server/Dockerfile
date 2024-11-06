# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker's caching
COPY requirements.txt .
# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code
COPY . .
# Expose the port that FastAPI runs on

EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]