FROM python:3.9-alpine

WORKDIR /code

ADD ./api.py .
ADD ./requirements.txt .

RUN apk update --no-cache \
	&& apk add tzdata

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=Asia/Bangkok

CMD uvicorn api:app --host 0.0.0.0 --port 8000
