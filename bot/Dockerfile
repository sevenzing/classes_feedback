FROM python:3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /bot/
#RUN python -m pip install mysqlclient 
COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/bot"

#CMD python bot.py
