FROM python:3.12

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip

COPY . .

RUN poetry install

EXPOSE 8002

# проверить
CMD ["python3", "./App/main.py"]
