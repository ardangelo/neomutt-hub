from config.defs import *

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
[[{p0}{p1}]]
path = {C_VDIRSYNCER_CALENDARS_DIR}{p0}/{p2}
''' # 0: label 1: calendar_label 2: collection
def gen_khalrc(caldav_accs):
	with open(L_KHALRC, 'w') as file:
		file.write(KHALRC_HEADER)
		for (label, acc) in caldav_accs.items():
			write_lines(file, [
				KHALRC_ENTRY.format(label, cal_label, cal_id)
				for (cal_label, cal_id) in acc['collections'].items()])
