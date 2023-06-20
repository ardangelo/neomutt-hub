import yaml
import os

# Local configurations
L_NEOMUTT_ACC_DIR = "neomutt/mutt.d/accounts/"
L_NEOMUTTRC_ADD = "neomutt/muttrc.add"

# Container targets
C_OFFLINEIMAP_ACC_DIR = "/hub/accounts/"
C_NEOMUTT_ACC_DIR = "/mutt/accounts/"

def gen_maildir(name, _):
	os.makedirs(L_NEOMUTT_ACC_DIR, exist_ok=True)
	with open(L_NEOMUTT_ACC_DIR + name, 'w') as file:
		file.write(
		f'set mbox_type = Maildir\n'
		f'set folder    = /hub/accounts/\n'
		f'set spoolfile = "+{name}/Inbox"')

def gen_neomuttrc_add(names):
	with open(L_NEOMUTTRC_ADD, 'w') as file:
		file.write(f'set folder = {C_OFFLINEIMAP_ACC_DIR}\n')
		file.write('\n'.join([
			f'source {C_NEOMUTT_ACC_DIR + name}'
			for name in names]) + '\n')

		file.write('\n'.join([
			f'folder-hook {name}/* source {C_NEOMUTT_ACC_DIR + name}'
			for name in names]) + '\n')

		file.write(f'set nm_default_url = "notmuch://{C_OFFLINEIMAP_ACC_DIR}"\n')
		file.write(f'virtual-mailboxes "Hub" "notmuch://?query=date:2022..today and \\\n')
		file.write(f'(')
		file.write(' or '.join([
			f'folder:{name}/Inbox'
			for name in names]) + ')\n')

		file.write(f'macro index,pager 0 "<change-vfolder>Hub<enter>"\n')
		file.write('\n'.join([
			f'macro index,pager {i} "<enter-command>source {C_NEOMUTT_ACC_DIR + name}<enter><change-folder>+{name}/Inbox<enter>"'
			for (i, name) in enumerate(names, 1)]) + '\n')

with open('accounts.yml', 'r') as accounts_yaml:
	accounts = yaml.safe_load(accounts_yaml)

for (name, acc) in accounts.items():
	if acc['type'] == 'maildir':
		gen_maildir(name, acc)

	gen_neomuttrc_add(accounts.keys())
