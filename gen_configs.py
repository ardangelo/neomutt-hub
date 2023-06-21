import yaml
import os

# Local configurations
L_NEOMUTT_ACC_DIR = "neomutt/mutt.d/accounts/"
L_NEOMUTTRC_ADD = "neomutt/muttrc.add"
L_NOTMUCHRC = "neomutt/notmuchrc"
L_OFFLINEIMAPRC = "offlineimap/offlineimaprc"
L_VDIRSYNCERRC = "neomutt/vdirsyncerrc"
L_KHARDRC = "neomutt/khardrc"
L_KHALRC = "neomutt/khalrc"

# Container targets
C_OFFLINEIMAP_ACC_DIR = "/hub/accounts/"
C_OFFLINEIMAP_MAILBOXES = "/hub/imap-mailboxes"
C_NEOMUTT_ACC_DIR = "/mutt/accounts/"
C_VDIRSYNCER_DIR = "/hub/vdirsyncer/"
C_VDIRSYNCER_CALENDARS_DIR = "/hub/calendars/"
C_VDIRSYNCER_CONTACTS_DIR = "/hub/contacts/"
C_KHAL_DIR = "/hub/khal/"

# Deferred placeholders to combine f-string and .format
_0 = '{0}'
_1 = '{1}'
_2 = '{2}'
_3 = '{3}'
_4 = '{4}'

def write_lines(file, lines):
	file.write(''.join(lines))

MAILDIR_ACCOUNT_BODY = f'''
set mbox_type = Maildir
set folder = {C_OFFLINEIMAP_ACC_DIR}
set spoolfile = "+{_0}/Inbox"
''' # 0: label
def gen_maildir_accounts(maildir_accs):
	os.makedirs(L_NEOMUTT_ACC_DIR, exist_ok=True)
	for label in maildir_accs.keys():
		with open(L_NEOMUTT_ACC_DIR + label, 'w') as file:
			file.write(MAILDIR_ACCOUNT_BODY.format(label))

NEOMUTTRC_HEADER = f'''
set folder = {C_OFFLINEIMAP_ACC_DIR}
'''
NEOMUTTRC_SOURCE_ENTRY = f'''
source {C_NEOMUTT_ACC_DIR}{_0}
''' # 0: label
NEOMUTTRC_FOLDER_HOOK_ENTRY = f'''
folder-hook {_0}/* source {C_NEOMUTT_ACC_DIR}{_0}
''' # 0: label
NEOMUTTRC_NOTMUCH_HEADER = f'''
set nm_default_url = "notmuch://{C_OFFLINEIMAP_ACC_DIR}"
virtual-mailboxes "Hub" "notmuch://?query=date:2022..today and \\
'''
NEOMUTTRC_NOTMUCH_HUB_CONDITION = f'''
folder:{_0}/Inbox
''' # 0: label
NEOMUTTRC_PAGE_0 = f'''
macro index,pager 0 "<change-vfolder>Hub<enter>"
'''
NEOMUTTRC_PAGE_ENTRY = f'''
macro index,pager {_0} "<enter-command>source {C_NEOMUTT_ACC_DIR}{_1}<enter><change-folder>+{_1}/Inbox<enter>"
''' # 0: index 1: label
def gen_neomuttrc_add(labels):
	with open(L_NEOMUTTRC_ADD, 'w') as file:
		file.write(NEOMUTTRC_HEADER)

		write_lines(file, [
			NEOMUTTRC_SOURCE_ENTRY.format(label)
			for label in labels])

		write_lines(file, [
			NEOMUTTRC_FOLDER_HOOK_ENTRY.format(label)
			for label in labels])

		file.write(NEOMUTTRC_NOTMUCH_HEADER)
		file.write('(' + ' or '.join([
			NEOMUTTRC_NOTMUCH_HUB_CONDITION.format(label).strip()
			for label in labels]) + ')')

		file.write(NEOMUTTRC_PAGE_0)
		write_lines(file, [
			NEOMUTTRC_PAGE_ENTRY.format(i, label)
			for (i, label) in enumerate(labels, 1)])

NOTMUCHRC_HEADER = f'''
[database]
path={C_OFFLINEIMAP_ACC_DIR}
[user]
name={_0}
primary_email={_1}
''' # 0: name 1: primary_email
NOTMUCHRC_EMAIL_ENTRY = f'''
other_email={_0}
''' # 0: other_email
NOTMUCHRC_FOOTER = f'''
[new]
tags=unread;inbox;
ignore=
[search]
exclude_tags=deleted;spam;
[maildir]
synchronize_flags=true
'''
def gen_notmuchrc(imap_accs):
	primary_name = list(imap_accs.values())[0]['name']
	primary_email = list(imap_accs.values())[0]['email']

	with open(L_NOTMUCHRC, 'w') as file:
		file.write(NOTMUCHRC_HEADER.format(primary_name, primary_email))
		write_lines(file, [
			NOTMUCHRC_EMAIL_ENTRY.format(acc["email"])
			for acc in list(imap_accs.values())[1:]])
		file.write(NOTMUCHRC_FOOTER)

OFFLINEIMAPRC_HEADER = f'''
[general]
# List of accounts to be synced, separated by a comma.
accounts = {_0}
maxsyncaccounts = 1
sockettimeout = 10
''' # 0: labels
OFFLINEIMAPRC_ACCOUNT_ENTRY = f'''
[Account {_0}]
# Identifier for the local repository; e.g. the maildir to be synced via IMAP.
localrepository = Local{_0}
# Identifier for the remote repository; i.e. the actual IMAP, usually non-local.
remoterepository = Remote{_0}
autorefresh = 1
quick = 10
postsynchook = curl -X POST http://host.docker.internal:4000/notmuch
maxage = 2

[Repository Local{_0}]
# Currently, offlineimap only supports maildir and IMAP for local repositories.
type = Maildir
# Where should the mail be placed?
localfolders = {C_OFFLINEIMAP_ACC_DIR}{_0}
maxage = 2

[Repository Remote{_0}]
# Remote repos can be IMAP or Gmail, the latter being a preconfigured IMAP.
type = IMAP
ssl = yes
remotehost = {_1}
remoteport = {_2}
remoteuser = {_3}
remotepass = {_4}
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

VDIRSYNCERRC_HEADER = f'''
[general]
status_path = "{C_VDIRSYNCER_DIR}/status/"
'''
VDIRSYNCER_CONTACT_ACCOUNT_ENTRY = f'''
[pair {_0}Contacts]
a = "{_0}ContactsLocal"
b = "{_0}ContactsRemote"
collections = ["from b"]
metadata = ["{_0}"]
conflict_resolution = "a wins"
[storage {_0}ContactsLocal]
type = "filesystem"
path = "{C_VDIRSYNCER_CONTACTS_DIR}/{_0}/"
fileext = ".vcf"
[storage {_0}ContactsRemote]
type = "carddav"
url = "{_1}"
username = "{_2}"
password = "{_3}"
''' # 0: label 1: host 2: user 3: password
VDIRSYNCER_CALENDAR_ACCOUNT_ENTRY = f'''
[pair {_0}Calendar]
a = "{_0}CalendarLocal"
b = "{_0}CalendarRemote"
collections = ["from b"]
metadata = ["{_0}", "blue"]
conflict_resolution = "a wins"
[storage {_0}CalendarLocal]
type = "filesystem"
path = "{C_VDIRSYNCER_CALENDARS_DIR}/{_0}"
fileext = ".ics"
[storage {_0}CalendarRemote]
type = "caldav"
url = "{_1}"
username = "{_2}"
password = "{_3}"
''' # 0: label 1: host 2: user 3: password
def gen_vdirsyncerrc(caldav_accs, carddav_accs):
	with open(L_VDIRSYNCERRC, 'w') as file:
		file.write(VDIRSYNCERRC_HEADER)
		write_lines(file, [
			VDIRSYNCER_CALENDAR_ACCOUNT_ENTRY.format(label,
				acc['host'], acc['user'], acc['password'])
			for (label, acc) in caldav_accs.items()])
		write_lines(file, [
			VDIRSYNCER_CONTACT_ACCOUNT_ENTRY.format(label,
				acc['host'], acc['user'], acc['password'])
			for (label, acc) in carddav_accs.items()])

KHALRC_HEADER = f'''
[sqlite]
path = {C_KHAL_DIR}/khal.db
[locale]
local_timezone = America/Chicago
default_timezone = America/Chicago
timeformat = %H:%M
dateformat = %Y-%m-%d
longdateformat = %Y-%m-%d
datetimeformat =  %Y-%m-%d
longdatetimeformat = %Y-%m-%dT%H:%M
firstweekday = 0
[default]
# in agenda/calendar display, shows all days even if there is no event
show_all_days = True
[calendars]
'''
KHALRC_ENTRY = f'''
[[{_0}{_1}]]
path = {C_VDIRSYNCER_CALENDARS_DIR}{_0}/{_2}
''' # 0: label 1: calendar_label 2: collection
def gen_khalrc(caldav_accs):
	with open(L_KHALRC, 'w') as file:
		file.write(KHALRC_HEADER)
		for (label, acc) in caldav_accs.items():
			write_lines(file, [
				KHALRC_ENTRY.format(label, cal_label, cal_id)
				for (cal_label, cal_id) in acc['collections'].items()])

KHARDRC_HEADER = f'''
[general]
editor = nano
merge_editor = nano
default_action = list
show_nicknames = no
[view]
theme = dark
[addressbooks]
'''
KHARDRC_ENTRY = f'''
[[{_0}]]
path = {C_VDIRSYNCER_CONTACTS_DIR}{_0}/{_2}/
''' # 0: label 1: card_label 2: collection
def gen_khardrc(carddav_accs):
	with open(L_KHARDRC, 'w') as file:
		file.write(KHARDRC_HEADER)
		for (label, acc) in carddav_accs.items():
			write_lines(file, [
				KHARDRC_ENTRY.format(label, card_label, card_id)
				for (card_label, card_id) in acc['collections'].items()])

with open('accounts.yml', 'r') as accounts_yaml:
	accounts = yaml.safe_load(accounts_yaml)

def filter_by_type(accs, types):
	return {k: v for (k, v) in accs.items() if v['type'] in types}

gen_maildir_accounts(filter_by_type(accounts, ['maildir']))
gen_neomuttrc_add(filter_by_type(accounts, ['imap', 'maildir']))
gen_notmuchrc(filter_by_type(accounts, ['imap']))
gen_offlineimaprc(filter_by_type(accounts, ['imap']))
gen_vdirsyncerrc(
	filter_by_type(accounts, ['caldav']),
	filter_by_type(accounts, ['carddav']))
gen_khalrc(filter_by_type(accounts, ['caldav']))
gen_khardrc(filter_by_type(accounts, ['carddav']))
