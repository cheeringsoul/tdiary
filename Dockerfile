FROM python:3.6
RUN mkdir /app
RUN mkdir /app/log
RUN mkdir /app/files
RUN mkdir /app/diary
#COPY . /app/ticket/
WORKDIR /app/diary
RUN pip install -r requirements.txt