#FROM python:3.10.13-alpine3.18
FROM python:3.10

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install -r  requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#
#
#
#
#ENV PYTHONUNBUFFERED 1
#
#COPY ./requirements.txt /tmp/requirements.txt
#COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#COPY ./main_app /main_app
#COPY . .
#WORKDIR /main_app
#EXPOSE 8000
#
#ARG DEV=false
#RUN python -m venv /py && \
#    /py/bin/pip install --upgrade pip && \
#    /py/bin/pip install -r /tmp/requirements.txt && \
#    if [ $DEV = "true" ]; \
#        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
#    fi && \
#    rm -rf /tmp
#RUN adduser --disabled-password --no-create-home django-user
#ENV PATH="/py/bin:$PATH"
#
#USER django-user
