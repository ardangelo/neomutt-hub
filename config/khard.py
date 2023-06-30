from config.defs import *

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
[[{p0}]]
path = {C_VDIRSYNCER_CONTACTS_DIR}{p0}/{p2}/
''' # 0: label 1: card_label 2: collection
def gen_khardrc(carddav_accs):
	with open(L_KHARDRC, 'w') as file:
		file.write(KHARDRC_HEADER)
		for (label, acc) in carddav_accs.items():
			write_lines(file, [
				KHARDRC_ENTRY.format(label, card_label, card_id)
				for (card_label, card_id) in acc['collections'].items()])
