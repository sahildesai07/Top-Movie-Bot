# Don't Remove Credit @Ultroid_official
# Subscribe YouTube Channel For Amazing Bot @dinesh12777
# Ask Doubt on telegram @UltroidxTeam

FROM python:3.10.8-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /Top-Movie-Bot
WORKDIR /Top-Movie-Bot
COPY . /Top-Movie-Bot
CMD ["python", "bot.py"]
