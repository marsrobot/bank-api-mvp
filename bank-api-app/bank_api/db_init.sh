#!/bin/bash

. ./env.sh

sh ./docker_build.sh

sudo docker run --rm -it \
  --env-file ./app.env \
  --entrypoint bash \
  ${IMAGE_NAME}:latest \
  -c "python3 manage.py drop_db; python3 manage.py create_db; python3 manage.py db init; python3 manage.py db migrate; python3 manage.py add_users"
