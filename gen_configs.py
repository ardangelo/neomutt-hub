import yaml
import os

from config.defs import *
from config.neomutt import gen_neomutt_maildir_accounts, gen_neomutt_imap_accounts, \
	gen_neomuttrc, gen_neomuttrc_accounts
from config.notmuch import gen_notmuchrc
from config.offlineimap import gen_offlineimaprc
from config.vdirsyncer import gen_vdirsyncerrc
from config.khal import gen_khalrc
from config.khard import gen_khardrc
from config.mailcap import gen_mailcaprc
from config.serve import gen_serverc

with open('accounts.yml', 'r') as accounts_yaml:
	accounts = yaml.safe_load(accounts_yaml)

def filter_by_type(accs, types):
	return {k: v for (k, v) in accs.items() if v['type'] in types}

os.makedirs(L_CONFIG_DIR, exist_ok=True)
os.makedirs(L_NEOMUTT_ACC_DIR, exist_ok=True)

gen_neomutt_maildir_accounts(filter_by_type(accounts, ['maildir']))
gen_neomutt_imap_accounts(filter_by_type(accounts, ['imap']))
gen_neomuttrc()
gen_neomuttrc_accounts(filter_by_type(accounts, ['imap', 'maildir']))
gen_notmuchrc(filter_by_type(accounts, ['imap']))
gen_offlineimaprc(filter_by_type(accounts, ['imap']))
gen_vdirsyncerrc(
	filter_by_type(accounts, ['caldav']),
	filter_by_type(accounts, ['carddav']))
gen_khalrc(filter_by_type(accounts, ['caldav']))
gen_khardrc(filter_by_type(accounts, ['carddav']))
gen_mailcaprc()
gen_serverc(filter_by_type(accounts, ['maildir']))
