#!/bin/bash

# Refresh OfflineIMAP
echo "Refreshing IMAP accounts..."
curl -X POST http://host.docker.internal:4001/offlineimap

# Start handler service
/usr/local/bin/python serve.py3 /hub/config/serverc 2>&1 > /serve.log &

# Run notmuch indexer
notmuch new

# Run vdirsyncer
yes | vdirsyncer discover
vdirsyncer sync

/bin/bash
