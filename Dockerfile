FROM python:slim

COPY ./tests/static/ /var/www/html/

COPY ./src/server/default.conf /

COPY ./src /

WORKDIR /

EXPOSE 80
EXPOSE 8080

CMD [ "python", "./server/main.py" ]