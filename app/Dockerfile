FROM python:3.8-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


RUN pip install --upgrade pip

WORKDIR usr/src/app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .