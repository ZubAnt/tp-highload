FROM python:slim

COPY ./tests/static/ /var/www/html/

COPY ./default.conf /

COPY ./src /

WORKDIR /

EXPOSE 80
EXPOSE 8080

USER root

CMD ["python3.6", "./server/main_v2.py"]