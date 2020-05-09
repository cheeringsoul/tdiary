FROM python:3.6
RUN mkdir /app
RUN mkdir /app/log
RUN mkdir /app/files
RUN mkdir /app/ticket
COPY . /app/ticket/
WORKDIR /app/ticket
RUN pip install -r requirements.txt