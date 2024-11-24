# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any necessary dependencies
RUN pip3 install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]