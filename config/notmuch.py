from config.defs import *

NOTMUCHRC_HEADER = f'''
[database]
path={C_OFFLINEIMAP_ACC_DIR}
[user]
name={p0}
primary_email={p1}
''' # 0: name 1: primary_email
NOTMUCHRC_EMAIL_ENTRY = f'''
other_email={p0}
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
