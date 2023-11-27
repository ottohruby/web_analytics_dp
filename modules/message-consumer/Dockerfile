# Use an official Python runtime as a parent image
FROM python:3.10-alpine

RUN apk update
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the command to run when the container starts
CMD ["python", "app.py"]