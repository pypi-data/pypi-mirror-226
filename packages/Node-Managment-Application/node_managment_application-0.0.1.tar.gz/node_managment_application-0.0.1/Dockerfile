FROM ubuntu:20.04
FROM python:3.9-slim-buster
RUN apt-get update
RUN apt-get install -y wget


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000
COPY . . 

CMD ["python",  "manage.py" , "runserver", "0.0.0.0:8000"]