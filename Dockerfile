FROM python:slim

COPY ./src /

COPY ./default.cong /

WORKDIR /

RUN mkdir -p /var/www/html


EXPOSE 80
EXPOSE 5000

CMD [ "python", "./server/main.py" ]