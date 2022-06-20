#!/bin/bash

. ./env.sh

sudo docker build --network=host -t ${IMAGE_NAME}:latest .