FROM python:3.7-alpine
RUN mkdir /app & mkdir -p /app/log & mkdir -p /app/files & mkdir -p /app/diary
COPY . /app/diary/
WORKDIR /app/diary
RUN pip install -r requirements.txt