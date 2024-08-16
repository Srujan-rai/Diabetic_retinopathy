FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt 
COPY . /app

EXPOSE 5000

ENV FLASK_APP=app

CMD [ "python","app.py" ]

