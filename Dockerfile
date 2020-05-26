FROM python:3.7-alpine
RUN mkdir /app & mkdir /app/log & mkdir /app/files & mkdir /app/diary
COPY . /app/diary/
WORKDIR /app/diary
RUN pip install -r requirements.txt