###########
# BUILDER #
###########

FROM python:3.9.1-buster

LABEL maintainer="Vadim Gazizov <smoke.kaliningrad@gmail.com>"

# create the appropriate directories
ENV HOME=/usr/src/app
WORKDIR $HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update -y
RUN apt install -y netcat

COPY . $APP_HOME

COPY docker/entrypoint.sh /entrypoint.sh
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

RUN chmod +x /entrypoint.sh

EXPOSE 80

HEALTHCHECK --interval=12s --timeout=12s --start-period=10s CMD curl --fail http://localhost/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
