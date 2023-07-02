from config.defs import *

def gen_serverc(maildir_accs):
	with open(L_SERVERC, 'w') as file:
		file.write('accounts:\n')
		file.write('\n'.join([f'  {label}: {C_OFFLINEIMAP_ACC_DIR}{label}/Inbox'
			for label in maildir_accs.keys()
		]))

