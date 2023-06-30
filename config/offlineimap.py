from config.defs import *

OFFLINEIMAPRC_HEADER = f'''
[general]
# List of accounts to be synced, separated by a comma.
accounts = {p0}
maxsyncaccounts = 1
sockettimeout = 10
''' # 0: labels
OFFLINEIMAPRC_ACCOUNT_ENTRY = f'''
[Account {p0}]
# Identifier for the local repository; e.g. the maildir to be synced via IMAP.
localrepository = Local{p0}
# Identifier for the remote repository; i.e. the actual IMAP, usually non-local.
remoterepository = Remote{p0}
autorefresh = 1
quick = 10
postsynchook = curl -X POST http://host.docker.internal:4000/notmuch
maxage = 2

[Repository Local{p0}]
# Currently, offlineimap only supports maildir and IMAP for local repositories.
type = Maildir
# Where should the mail be placed?
localfolders = {C_OFFLINEIMAP_ACC_DIR}{p0}
maxage = 2

[Repository Remote{p0}]
# Remote repos can be IMAP or Gmail, the latter being a preconfigured IMAP.
type = IMAP
ssl = yes
remotehost = {p1}
remoteport = {p2}
remoteuser = {p3}
remotepass = {p4}
maxconnections = 5
holdconnectionopen = yes
keepalive = 60
idlefolder = ['INBOX']
sslcacertfile = /etc/ssl/certs/ca-certificates.crt
maxage = 2
''' # 0: label 1: imap_host 2: imap_port 3: imap_user 4: imap_pass
OFFLINEIMAPRC_FOOTER = f'''
# Automatic mailbox generation for mutt
[mbnames]
enabled  = yes
filename = {C_OFFLINEIMAP_MAILBOXES}
header   = "mailboxes "
peritem  = "+%(accountname)s/%(foldername)s"
sep      = " "
footer   = "\\n"
'''
def gen_offlineimaprc(imap_accs):
	with open(L_OFFLINEIMAPRC, 'w') as file:
		file.write(OFFLINEIMAPRC_HEADER.format(','.join([
			label
			for label in imap_accs.keys()
		])))
		write_lines(file, [
			OFFLINEIMAPRC_ACCOUNT_ENTRY.format(
				label, acc['imap-host'], acc['imap-port'],
				acc['imap-user'], acc['imap-password'])
			for (label, acc) in imap_accs.items()])
		file.write(OFFLINEIMAPRC_FOOTER)
