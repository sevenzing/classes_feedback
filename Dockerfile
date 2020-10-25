FROM python:3.7
WORKDIR /classes_feedback/
COPY requirements.txt /classes_feedback/
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py migrate

