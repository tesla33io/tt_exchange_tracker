FROM python:3.8

WORKDIR /bot

COPY requirenments.txt /bot/
RUN pip install -r requirenments.txt

COPY . /bot/

CMD python bot.py