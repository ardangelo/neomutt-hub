import os

# Local configurations
L_CONFIG_DIR = f"{os.getenv('HOME')}/hub/config/"
L_NEOMUTT_ACC_DIR = f"{L_CONFIG_DIR}/accounts/"
L_NEOMUTTRC = f"{L_CONFIG_DIR}muttrc"
L_NEOMUTTRC_ACCOUNTS = f"{L_CONFIG_DIR}muttrc.accounts"
L_NOTMUCHRC = f"{L_CONFIG_DIR}notmuchrc"
L_OFFLINEIMAPRC = f"{L_CONFIG_DIR}offlineimaprc"
L_VDIRSYNCERRC = f"{L_CONFIG_DIR}vdirsyncerrc"
L_KHARDRC = f"{L_CONFIG_DIR}khardrc"
L_KHALRC = f"{L_CONFIG_DIR}khalrc"
L_MAILCAPRC = f"{L_CONFIG_DIR}mailcaprc"

# Container targets
C_BASE_DIR = "/hub/"
C_CONFIG_DIR = f"{C_BASE_DIR}config/"
C_OFFLINEIMAP_ACC_DIR = f"{C_BASE_DIR}accounts/"
C_OFFLINEIMAP_MAILBOXES = f"{C_BASE_DIR}imap-mailboxes"
C_NEOMUTTRC_ACCOUNTS = f"{C_CONFIG_DIR}/muttrc.accounts"
C_NEOMUTT_ACC_DIR = f"{C_CONFIG_DIR}accounts/"
C_VDIRSYNCER_DIR = f"{C_BASE_DIR}vdirsyncer/"
C_VDIRSYNCER_CALENDARS_DIR = f"{C_BASE_DIR}calendars/"
C_VDIRSYNCER_CONTACTS_DIR = f"{C_BASE_DIR}contacts/"
C_KHAL_DIR = f"{C_BASE_DIR}khal/"

# Deferred placeholders to combine f-string and .format
p0 = '{0}'
p1 = '{1}'
p2 = '{2}'
p3 = '{3}'
p4 = '{4}'

def write_lines(file, lines):
	file.write(''.join(lines))
