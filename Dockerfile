FROM python:3.9-bullseye

COPY . /docqa_plugin

WORKDIR /docqa_plugin

RUN pip3 install -r requirements.txt

RUN python3 main.py
