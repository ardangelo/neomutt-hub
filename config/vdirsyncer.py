from config.defs import *

VDIRSYNCERRC_HEADER = f'''
[general]
status_path = "{C_VDIRSYNCER_DIR}/status/"
'''
VDIRSYNCER_CONTACT_ACCOUNT_ENTRY = f'''
[pair {p0}Contacts]
a = "{p0}ContactsLocal"
b = "{p0}ContactsRemote"
collections = ["from b"]
metadata = ["{p0}"]
conflict_resolution = "a wins"
[storage {p0}ContactsLocal]
type = "filesystem"
path = "{C_VDIRSYNCER_CONTACTS_DIR}/{p0}/"
fileext = ".vcf"
[storage {p0}ContactsRemote]
type = "carddav"
url = "{p1}"
username = "{p2}"
password = "{p3}"
''' # 0: label 1: host 2: user 3: password
VDIRSYNCER_CALENDAR_ACCOUNT_ENTRY = f'''
[pair {p0}Calendar]
a = "{p0}CalendarLocal"
b = "{p0}CalendarRemote"
collections = ["from b"]
metadata = ["{p0}", "blue"]
conflict_resolution = "a wins"
[storage {p0}CalendarLocal]
type = "filesystem"
path = "{C_VDIRSYNCER_CALENDARS_DIR}/{p0}"
fileext = ".ics"
[storage {p0}CalendarRemote]
type = "caldav"
url = "{p1}"
username = "{p2}"
password = "{p3}"
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
