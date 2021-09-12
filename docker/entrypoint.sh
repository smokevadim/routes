#!/bin/bash
set -e

if [ "$WAITING_DATABASE" = true ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

cd $home

uvicorn main:app --host 0.0.0.0 --port 8500 --access-log

#exec "$@"