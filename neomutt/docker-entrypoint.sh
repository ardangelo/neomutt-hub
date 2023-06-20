#!/bin/bash

touch /hub/imap-mailboxes

# Run notmuch service
notmuch new
/usr/local/bin/python serve_command.py3 \
    /notmuch /usr/bin/notmuch new --verbose 2>&1 > /notmuch.log &

/bin/bash
