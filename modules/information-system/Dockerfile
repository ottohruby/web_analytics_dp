# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

# Copy the rest of the application code into the container
COPY . .

EXPOSE 8080

# Set the command to run when the container starts
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]
