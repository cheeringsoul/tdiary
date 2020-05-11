FROM python:3.7-alpine
RUN mkdir /app
RUN mkdir /app/log
RUN mkdir /app/files
RUN mkdir /app/diary
COPY requirements.txt /app/diary/
WORKDIR /app/diary
RUN pip install -r requirements.txt