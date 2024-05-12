FROM python:3.10-slim-buster

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]
