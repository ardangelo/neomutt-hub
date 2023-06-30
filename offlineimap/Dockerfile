FROM python:2.7.17-alpine

# Install dependencies
RUN apk update && apk add \
	curl

# Install OfflineIMAP
RUN pip install offlineimap

# Configure OfflineIMAP
RUN ln -s /hub/config/offlineimaprc /root/.offlineimaprc

# Configure OfflineIMAP service
COPY serve_command.py2 /serve_command.py2
EXPOSE 4000

# Define the entry point
ENTRYPOINT ["/usr/local/bin/python2", "/serve_command.py2", \
	"/offlineimap", "/usr/local/bin/offlineimap -o"]
