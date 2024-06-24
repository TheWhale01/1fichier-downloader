FROM python:3

RUN apt update && apt install firefox-esr -y
COPY ./requirements.txt /tmp
RUN python3 -m pip install -r /tmp/requirements.txt --break-system-packages
