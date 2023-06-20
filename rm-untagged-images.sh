#!/bin/bash

ids=$(docker images | grep '<none>' | tr -s ' ' | cut -d ' ' -f 3)
for id in $ids; do
	docker image rm $id
done
