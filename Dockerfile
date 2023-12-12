# syntax=docker/dockerfile:1

FROM python:3.12.1-bullseye
WORKDIR /code
COPY ./docker-scripts.sh /code/docker-scripts.sh
RUN chmod +x /code/docker-scripts.sh && /code/docker-scripts.sh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
ADD . /code