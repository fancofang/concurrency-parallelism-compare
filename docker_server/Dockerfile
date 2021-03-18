FROM alpine

WORKDIR /usr/src/app

RUN apk add --no-cache python3 py3-pip \
    && pip install --no-cache-dir flask

COPY . .

ENV FLASK_APP=app.py

CMD ["flask","run","--host=0.0.0.0","--port=8000"]

