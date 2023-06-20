FROM python:3-alpine

# Install dependencies
RUN apk update && apk add \
	tini curl bash

# Install neomutt, notmuch, khal, khard
RUN apk add \
	neomutt notmuch khal
RUN apk add --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing \
	khard

# Install editors
RUN apk add nano

# Configure notmuch
COPY notmuchrc /root/.notmuch-config
COPY serve_command.py3 /serve_command.py3
EXPOSE 4000

# Configure Neomutt
COPY muttrc.base /muttrc.base
COPY muttrc.add /muttrc.add
ADD mutt.d /mutt
RUN ln -s /muttrc.base /root/.muttrc

# Configure entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Define the entry point
ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]
