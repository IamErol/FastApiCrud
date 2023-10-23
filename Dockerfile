#FROM python:3.10.13-alpine3.18
FROM python:3.10

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r  requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

