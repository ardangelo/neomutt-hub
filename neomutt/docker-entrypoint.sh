#!/bin/bash

# Run notmuch service
mkdir -p /hub/mailboxes
notmuch new
/usr/local/bin/python serve_command.py3 \
    /notmuch /usr/bin/notmuch new --verbose 2>&1 > /notmuch.log &

/bin/bash
