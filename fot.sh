#!/bin/bash

function prepare() {
	#sudo docker-compose pull
	sudo docker-compose up -d
	sudo docker-compose ps
	sudo docker cp tidbdockercompose_pd0_1:/pd-ctl ./  
	echo "set global tidb_disable_txn_auto_retry = off;" | mysql -h 127.0.0.1 -P 4000 -u root
	echo "create database sbtest;" | mysql -h 127.0.0.1 -P 4000 -u root
	sysbench --config-file=sysbench.conf oltp_point_select --tables=3 --table-size=1000 prepare
}

function start() {
	sudo docker pause tidbdockercompose_tikv1_1
	./fot.py
}

function stop() {
	sudo docker-compose down
	sudo git clean -xfd
}
