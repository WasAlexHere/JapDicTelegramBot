FROM python:3.11
RUN mkdir /japan_dict_bot
COPY . /japan_dict_bot
#ARG BOT_API_KEY=.env
#COPY ${BOT_API_KEY} .env
WORKDIR /japan_dict_bot
RUN pip3 install -r requirements.txt
CMD ["python3", "bot.py"]