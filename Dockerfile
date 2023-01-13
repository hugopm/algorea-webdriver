# syntax=docker/dockerfile:1

FROM python:bullseye

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y firefox-esr && rm -rf /var/lib/apt/lists/*

COPY . .
CMD ["python3", "main.py"]
