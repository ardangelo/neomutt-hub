#!/bin/bash

# Refresh OfflineIMAP
echo "Refreshing IMAP accounts..."
curl -X POST http://host.docker.internal:4001/offlineimap

# Run notmuch service
notmuch new
/usr/local/bin/python serve_command.py3 \
    /notmuch /usr/bin/notmuch new --verbose 2>&1 > /notmuch.log &

/bin/bash
