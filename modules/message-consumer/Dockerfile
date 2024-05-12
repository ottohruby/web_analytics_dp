FROM python:3.10-alpine

RUN apk update
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r ./requirements.txt

COPY . .

CMD ["python", "app.py"]
