#!/bin/bash

docker run -it -p 4001:4000 --add-host=host.docker.internal:host-gateway \
	-v $HOME/hub:/hub offlineimap:latest

