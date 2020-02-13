FROM python:3.8-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add --no-cache \
        python3-dev \
        build-base \
    && \
    pip install \
        -r requirements.txt

COPY . .

EXPOSE 9500

CMD [ "/usr/local/bin/python", "./app.py" ]