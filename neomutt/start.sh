#!/bin/bash

docker run -it -p 4000:4000 --add-host=host.docker.internal:host-gateway \
	-v $HOME/hub:/hub neomutt:latest

