# syntax=docker/dockerfile:1

FROM python:3.13.0-alpine3.20
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apk add gcc python3-dev musl-dev linux-headers
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
ADD . /code
