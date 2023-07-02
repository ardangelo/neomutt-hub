.PHONY: start attach stop clean

all: stamp-configs stamp-neomutt stamp-offlineimap

stamp-configs: accounts.yml
	python gen_configs.py
	touch stamp-configs

stamp-neomutt: neomutt/Dockerfile
	docker build -t neomutt neomutt
	touch stamp-neomutt

stamp-offlineimap: offlineimap/Dockerfile
	docker build -t offlineimap offlineimap
	touch stamp-offlineimap

start: stamp-neomutt stamp-offlineimap
	docker-compose up --detach

attach:
	docker attach hub_neomutt_1

stop:
	docker-compose down
