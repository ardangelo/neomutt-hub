#!/bin/bash

# Stop all containers
# docker stop $(docker ps -a -q)

ids=$(docker container ls -a | tail -n +2 | tr -s ' ' | cut -d ' ' -f 1)

for id in $ids; do
	docker container rm $id
done
