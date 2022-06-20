#!/bin/bash

. ./env.sh

sudo docker stop ${CONTAINER_NAME}
sudo docker rm -f ${CONTAINER_NAME}

sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT

sudo docker run -it -d \
  --name=${CONTAINER_NAME} \
  --restart unless-stopped \
  --env-file ./app.env \
  -p 0.0.0.0:8080:80 \
  ${IMAGE_NAME}:latest
