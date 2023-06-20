import yaml
import os

# Local configurations
L_NEOMUTT_ACC_DIR = "neomutt/mutt.d/accounts/"
L_NEOMUTTRC_ADD = "neomutt/muttrc.add"
L_NOTMUCHRC = "neomutt/notmuchrc"

# Container targets
C_OFFLINEIMAP_ACC_DIR = "/hub/accounts/"
C_NEOMUTT_ACC_DIR = "/mutt/accounts/"

def gen_maildir(label, _):
	os.makedirs(L_NEOMUTT_ACC_DIR, exist_ok=True)
	with open(L_NEOMUTT_ACC_DIR + label, 'w') as file:
		file.write(
		f'set mbox_type = Maildir\n'
		f'set folder    = /hub/accounts/\n'
		f'set spoolfile = "+{label}/Inbox"')

def gen_neomuttrc_add(labels):
	with open(L_NEOMUTTRC_ADD, 'w') as file:
		file.write(f'set folder = {C_OFFLINEIMAP_ACC_DIR}\n')
		file.write('\n'.join([
			f'source {C_NEOMUTT_ACC_DIR + label}'
			for label in labels]) + '\n')

		file.write('\n'.join([
			f'folder-hook {label}/* source {C_NEOMUTT_ACC_DIR + label}'
			for label in labels]) + '\n')

		file.write(f'set nm_default_url = "notmuch://{C_OFFLINEIMAP_ACC_DIR}"\n')
		file.write(f'virtual-mailboxes "Hub" "notmuch://?query=date:2022..today and \\\n')
		file.write(f'(')
		file.write(' or '.join([
			f'folder:{label}/Inbox'
			for label in labels]) + ')\n')

		file.write(f'macro index,pager 0 "<change-vfolder>Hub<enter>"\n')
		file.write('\n'.join([
			f'macro index,pager {i} "<enter-command>source {C_NEOMUTT_ACC_DIR + label}<enter><change-folder>+{label}/Inbox<enter>"'
			for (i, label) in enumerate(labels, 1)]) + '\n')

def gen_notmuchrc(name, accs):
	with open(L_NOTMUCHRC, 'w') as file:
		file.write(f'[database]\npath={C_OFFLINEIMAP_ACC_DIR}\n')
		file.write(f'[user]\nname={name}\n')
		file.write(f'primary_email={accs[0]["email"]}\n')
		file.write('\n'.join([
			f'other_email={acc["email"]}\n'
			for accs in accs[1:]]) + '\n')
		file.write(f'[new]\ntags=unread;inbox;\nignore=\n')
		file.write(f'[search]\nexclude_tags=deleted;spam;\n')
		file.write(f'[maildir]\nsynchronize_flags=true\n')

with open('accounts.yml', 'r') as accounts_yaml:
	accounts = yaml.safe_load(accounts_yaml)

for (name, acc) in accounts.items():
	if acc['type'] == 'maildir':
		gen_maildir(name, acc)

gen_neomuttrc_add(accounts.keys())

imap_accounts = [v for v in accounts.values() if v['type'] == 'imap']
primary_name = imap_accounts[0]['name']
gen_notmuchrc(primary_name, imap_accounts)
