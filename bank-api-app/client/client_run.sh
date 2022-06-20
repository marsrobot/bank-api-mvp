#!/bin/bash

. ./env.sh

sudo docker build --network=host -t ${IMAGE_NAME}:latest .

sudo docker run --rm -it \
  --name=${CONTAINER_NAME} \
  --entrypoint bash \
  ${IMAGE_NAME}:latest \
  -c "python3 client.py"
