FROM ubuntu

FROM python:3.8-slim-buster

WORKDIR /

EXPOSE 9412

ENV DEBIAN_FRONTEND noninteractive
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9412"]
