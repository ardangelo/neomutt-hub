.PHONY: start attach stop clean

all: stamp-config stamp-neomutt stamp-offlineimap

stamp-config: accounts.yml
	python gen_configs.py
	touch stamp-config

stamp-neomutt: neomutt/Dockerfile
	cp serve_command.py3 neomutt
	docker build -t neomutt neomutt
	touch stamp-neomutt

stamp-offlineimap: offlineimap/Dockerfile
	cp serve_command.py2 offlineimap
	docker build -t offlineimap offlineimap
	touch stamp-offlineimap

start: stamp-neomutt stamp-offlineimap
	docker-compose up --detach

attach:
	docker attach hub_neomutt_1

stop:
	docker-compose down
