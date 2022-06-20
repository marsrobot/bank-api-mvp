#!/bin/bash

. ./env.sh

sudo docker stop $CONTAINER_NAME
sudo docker rm -f $CONTAINER_NAME

sudo iptables -I INPUT -p tcp --dport 3306 -j ACCEPT
sudo iptables -I INPUT -p udp --dport 3306 -j ACCEPT

export DATA_DIR="/srv"
echo "Data directory: " ${DATA_DIR}/var/lib/mysql
sudo mkdir -p ${DATA_DIR}/var/lib/mysql

echo "${MYSQL_ROOT_PASSWORD}"


sudo docker run -it -d \
  --restart unless-stopped \
  --privileged \
  --name $CONTAINER_NAME \
  --env MYSQL_ROOT_PASSWORD="${MYSQL_ROOT_PASSWORD}" \
  --env MYSQL_PASSWORD="${MYSQL_NORMALUSER_PASSWORD}" \
  --env MYSQL_USER=*** \
  -v ${DATA_DIR}/var/lib/mysql:/var/lib/mysql:rw \
  -p 3306:3306 \
  --entrypoint sh \
  mysql:8.0.28 \
  -c "exec docker-entrypoint.sh mysqld --default-authentication-plugin=mysql_native_password" \
  --binlog_expire_logs_seconds=3600 \
  --innodb_buffer_pool_instances=1 \
  --innodb_buffer_pool_size=1024M \
  --innodb_file_per_table=ON \
  --innodb_flush_log_at_trx_commit=2 \
  --innodb_flush_method=O_DIRECT \
  --innodb_log_file_size=512MB \
  --innodb_read_io_threads=8 \
  --innodb_write_io_threads=4
