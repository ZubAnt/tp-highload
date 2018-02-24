FROM python:slim

COPY ./src /

COPY ./src/server/default.conf /

WORKDIR /

RUN mkdir -p /var/www/html


EXPOSE 80
EXPOSE 8080

CMD [ "python", "./server/main.py" ]