FROM python:3.9

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8002

CMD ["python3", "./App/main.py"]
