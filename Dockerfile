FROM python:slim

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

#COPY ./tests/static/ /var/www/html/

COPY ./default.conf /

COPY ./src /

WORKDIR /

EXPOSE 80
EXPOSE 8080

USER root

CMD ["python3.6", "./server/main.py"]