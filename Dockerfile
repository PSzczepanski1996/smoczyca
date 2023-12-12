# syntax=docker/dockerfile:1

FROM python:3.12.1-bullseye
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
ADD . /code