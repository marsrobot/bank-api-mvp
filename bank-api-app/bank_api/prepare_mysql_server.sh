#!/bin/bash

. ./env.sh

echo ${MYSQL_ROOT_PASSWORD}

mysql -u root -p${MYSQL_ROOT_PASSWORD} -h MYSERVERIP -e "DROP DATABASE IF EXISTS newbank"
mysql -u root -p${MYSQL_ROOT_PASSWORD} -h MYSERVERIP -e "CREATE DATABASE IF NOT EXISTS newbank"
