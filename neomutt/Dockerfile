FROM python:3-alpine

# Install dependencies
RUN apk update && apk add \
	tini curl bash

# Install neomutt, notmuch, khal, khard
RUN apk add \
	neomutt notmuch khal vdirsyncer
RUN apk add --repository=https://dl-cdn.alpinelinux.org/alpine/edge/testing \
	khard

# Install editors and viewers
RUN apk add nano w3m
ENV EDITOR=nano

# Configure notmuch
RUN ln -s /hub/config/notmuchrc /root/.notmuch-config
COPY serve_command.py3 /serve_command.py3
EXPOSE 4000

# Configure Neomutt and mailcap
RUN ln -s /hub/config/muttrc /root/.muttrc \
 && ln -s /hub/config/mailcaprc /root/.mailcap

# Configure WebDAV
RUN mkdir -p /root/.config/vdirsyncer /root/.config/khard /root/.config/khal \
 && ln -s /hub/config/vdirsyncerrc /root/.config/vdirsyncer/config \
 && ln -s /hub/config/khardrc /root/.config/khard/khard.conf \
 && ln -s /hub/config/khalrc /root/.config/khal/config

# Configure entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh

# Define the entry point
ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]
