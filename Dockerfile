FROM python:3.9-slim

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn