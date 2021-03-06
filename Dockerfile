FROM python:3.9
WORKDIR /usr/src/app
COPY app/requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./app /usr/src/app
