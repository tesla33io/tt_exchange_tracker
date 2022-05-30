FROM python:3.8

ENV BOT_TOKEN=<bot token here>
ENV DB_TOKEN=<mongodb token here>

WORKDIR /bot

COPY requirenments.txt /bot/
RUN pip install -r requirenments.txt

COPY . /bot/

CMD python bot.py
