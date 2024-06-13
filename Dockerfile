# pull official base image
FROM python:3.9.2-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

# install psycopg2 dependencies
RUN apk update \
    && apk add libffi-dev postgresql-dev wkhtmltopdf gcc python3-dev musl-dev py-pip jpeg-dev zlib-dev \
    && apk add libressl-dev perl rust libmagic pango openjpeg-dev g++ ffmpeg

RUN apk --no-cache add \
    icu-dev \
    gettext \
    gettext-dev

RUN apk --no-cache add glib-dev poppler-glib vips-dev vips-tools poppler-utils

# copy requirements file
COPY ./requirements.txt .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# create directory for the app user
RUN mkdir -p /home/app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/static $APP_HOME/media $APP_HOME/locale
WORKDIR $APP_HOME

# copy entrypoint.sh and set permissions
COPY ./entrypoint.sh $APP_HOME
RUN chmod +x /home/app/web/entrypoint.sh

# set entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
