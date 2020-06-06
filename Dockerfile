FROM python:latest
ADD . /api/todo
WORKDIR /api/todo
RUN pip install flask pymongo requests
