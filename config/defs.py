import os

# Local configurations
L_CONFIG_DIR = f"{os.getenv('HOME')}/hub/config/"
L_NEOMUTT_ACC_DIR = f"{L_CONFIG_DIR}mutt/accounts/"
L_NEOMUTTRC = f"{L_CONFIG_DIR}muttrc"
L_NEOMUTTRC_ACCOUNTS = f"{L_CONFIG_DIR}muttrc.accounts"
L_NOTMUCHRC = f"{L_CONFIG_DIR}notmuchrc"
L_OFFLINEIMAPRC = f"{L_CONFIG_DIR}offlineimaprc"
L_VDIRSYNCERRC = f"{L_CONFIG_DIR}vdirsyncerrc"
L_KHARDRC = f"{L_CONFIG_DIR}khardrc"
L_KHALRC = f"{L_CONFIG_DIR}khalrc"
L_MAILCAPRC = f"{L_CONFIG_DIR}mailcaprc"
L_SERVERC = f"{L_CONFIG_DIR}serverc"

# Container targets
C_CONFIG_DIR = "/hub/config/"
C_OFFLINEIMAP_ACC_DIR = "/hub/accounts/"
C_OFFLINEIMAP_MAILBOXES = "/hub/imap-mailboxes"
C_NEOMUTTRC_ACCOUNTS = "/hub/config/muttrc.accounts"
C_NEOMUTT_DIR = "/hub/config/mutt/"
C_NEOMUTT_ACC_DIR = f"{C_NEOMUTT_DIR}accounts/"
C_VDIRSYNCER_DIR = "/hub/vdirsyncer/"
C_VDIRSYNCER_CALENDARS_DIR = "/hub/calendars/"
C_VDIRSYNCER_CONTACTS_DIR = "/hub/contacts/"
C_KHAL_DIR = "/hub/khal/"

# Deferred placeholders to combine f-string and .format
p0 = '{0}'
p1 = '{1}'
p2 = '{2}'
p3 = '{3}'
p4 = '{4}'

def write_lines(file, lines):
	file.write(''.join(lines))
