from config.defs import *

MAILDIR_ACCOUNT_BODY = f'''
set mbox_type = Maildir
set folder = {C_OFFLINEIMAP_ACC_DIR}
set spoolfile = "+{p0}/Inbox"
''' # 0: label
def gen_neomutt_maildir_accounts(maildir_accs):
	for label in maildir_accs.keys():
		with open(L_NEOMUTT_ACC_DIR + label, 'w') as file:
			file.write(MAILDIR_ACCOUNT_BODY.format(label))

IMAP_ACCOUNT_BODY = f'''
set sendmail = "/usr/bin/msmtp -a {p0}"
set realname = "{p1}"
set from = "{p2}"
set mbox_type = Maildir
set spoolfile = "+{p0}/Inbox"
set record = "+{p0}/Sent"
set postponed = "+{p0}/Drafts"
''' # 0: label 1: name 2: email
def gen_neomutt_imap_accounts(imap_accs):
	for (label, acc) in imap_accs.items():
		with open(L_NEOMUTT_ACC_DIR + label, 'w') as file:
			file.write(IMAP_ACCOUNT_BODY.format(label, acc['name'], acc['email']))

NEOMUTTRC_BODY = f'''
source {C_NEOMUTTRC_ACCOUNTS}
source {C_OFFLINEIMAP_MAILBOXES}

#Speed up folder switch
set sleep_time = 0
set timeout = 30

# Mutt can cache headers of messages so they need to be downloaded just once.
# This greatly improves speed when opening folders again later.
#set header_cache     = {C_NEOMUTT_DIR}cache/headers
set message_cachedir = {C_NEOMUTT_DIR}cache/bodies

# Fetch new mails via offlineimap
macro index,pager z "! echo 'Refreshing IMAP accounts, please wait...'; curl -X POST http://host.docker.internal:4001/offlineimap<enter>" "Refresh offlineimap"

# Khard commands
#complete email addresses by pressing the Tab-key in mutt's new mail dialog
set query_command= "khard email --parsable '%s'"
bind editor <Tab> complete-query
bind editor ^T    complete
#add email addresses to khard's address book
#macro index,pager A "<pipe-message>khard add-email<return>" "add the sender email address to khard"

# Mutt bindings
bind index <tab> sidebar-toggle-visible
bind index n   sidebar-next
bind index p     sidebar-prev
bind index <return>  sidebar-open
bind index f next-entry
bind index b previous-entry

#bind pager f <next-line>
#bind pager b <previous-line>
#bind pager F <forward-message>
#bind pager r <reply>
#bind pager w <flag-message>
#bind pager i <save-entry>
#bind pager <delete> <delete-entry>

# Mutt Behaviour
set sig_on_top        = yes
set mime_forward      = ask-yes
set move              = no
set sort              = 'threads'
set sort_aux          = 'reverse-last-date-received'
set sort_re           = yes
set pager_stop        = yes
set pager_index_lines = 20
set quit              = ask-yes
set fast_reply        = yes
set include           = yes
set reverse_name      = yes
set pager_context     = 3     # number of context lines to show
set pager_stop        = yes   # don't go to next message automatically
set menu_scroll       = yes   # scroll in menus
set tilde             = yes   # show tildes like in vim
set markers           = no    # no ugly plus signs
set edit_headers      = yes

auto_view text/html
auto_view text/plain

# Ignore all headers
ignore *
# Then un-ignore the ones I want to see
unignore From:
unignore To:
unignore Reply-To:
unignore Mail-Followup-To:
unignore Subject:
unignore Date:
unignore Organization:
unignore Newsgroups:
unignore CC:
unignore BCC:
unignore Message-ID:
unignore X-Mailer:
unignore User-Agent:
unignore X-Junked-Because:
unignore X-SpamProbe:
unignore X-Virus-hagbard:
# Now order the visable header lines
hdr_order From: Subject: To: CC: BCC: Reply-To: Mail-Followup-To: Date: Organization: User-Agent: X-Mailer:

set index_format = "%S %-20.20F %-20.20s %<[y?%<[m?%<[d?%[%H:%M ]&%[%a %d]>&%[%b %d]>&%[%m/%y ]>"
set xterm_set_titles  = yes

# Sidebar
set sidebar_visible=no
set sidebar_divider_char='|'
set mail_check_stats=yes
set sidebar_format='%B%?F? [%F]?%* %?N?%N/?%S'
set sidebar_short_path=yes
set sidebar_delim_chars='/'
set sidebar_folder_indent=yes
set sidebar_indent_string="  "
set sidebar_width=25
set sidebar_sort_method=path

# View attachments properly.
auto_view text/html
auto_view text/plain
bind attach <return> view-mailcap

# 'L' performs a notmuch query, showing only the results
macro index L \\
  "<enter-command>unset wait_key<enter><shell-escape>read -p 'notmuch query: ' x; \\
  echo \$x >~/.cache/mutt_terms<enter><limit>~i \\
  \\"\`notmuch search --output=messages \$(cat ~/.cache/mutt_terms) | \\
    head -n 600 | perl -le '@a=<>;chomp@a;s/\^id:// for@a;$,=\"|\";print@a'\`\\"<enter>" \\
  "show only messages matching a notmuch pattern"
# 'a' shows all messages again (supersedes default <alias> binding)
macro index a "<limit>all\\n" "show all messages (undo limit)"

color index      brightgreen    default  ~F # Markierte Nachrichten
color index      red            default  ~N # Neue Nachrichten
color index      red            default  ~O # Ungelesene Nachrichten

### Header
color header default default "^from:"
color header default default "^to:"
color header default default "^cc:"
color header default default "^date:"
color header default default "^newsgroups:"
color header default default "^reply-to:"
color header default default "^subject:"
color header default default "^x-spam-rule:"
color header default default "^x-mailer:"
color header default default "^message-id:"
color header default default "^Organization:"
color header default default "^Organisation:"
color header default default "^User-Agent:"
color header default default "^message-id: .*pine"
color header default default "^X-Fnord:"
color header default default "^X-WebTV-Stationery:"
color header default default "^x-spam-rule:"
color header default default "^x-mailer:"
color header default default "^message-id:"
color header default default "^Organization:"
color header default default "^Organisation:"
color header default default "^User-Agent:"
color header default default "^message-id: .*pine"
color header default default "^X-Fnord:"
color header default default "^X-WebTV-Stationery:"
color header default default "^X-Message-Flag:"
color header default default "^X-Spam-Status:"
color header default default "^X-SpamProbe:"
color header default default "^X-SpamProbe: SPAM"
'''
def gen_neomuttrc():
	with open(L_NEOMUTTRC, 'w') as file:
		file.write(NEOMUTTRC_BODY)

NEOMUTTRC_ACCOUNTS_HEADER = f'''
set folder = {C_OFFLINEIMAP_ACC_DIR}
'''
NEOMUTTRC_ACCOUNTS_SOURCE_ENTRY = f'''
source {C_NEOMUTT_ACC_DIR}{p0}
''' # 0: label
NEOMUTTRC_ACCOUNTS_FOLDER_HOOK_ENTRY = f'''
folder-hook {p0}/* source {C_NEOMUTT_ACC_DIR}{p0}
''' # 0: label
NEOMUTTRC_ACCOUNTS_NOTMUCH_HEADER = f'''
set nm_default_url = "notmuch://{C_OFFLINEIMAP_ACC_DIR}"
virtual-mailboxes "Hub" "notmuch://?query=date:2022..today and \\
'''
NEOMUTTRC_ACCOUNTS_NOTMUCH_HUB_CONDITION = f'''
folder:{p0}/Inbox
''' # 0: label
NEOMUTTRC_ACCOUNTS_PAGE_0 = f'''
macro index,pager 0 "<change-vfolder>Hub<enter>"
'''
NEOMUTTRC_ACCOUNTS_PAGE_ENTRY = f'''
macro index,pager {p0} "<enter-command>source {C_NEOMUTT_ACC_DIR}{p1}<enter><change-folder>+{p1}/Inbox<enter>"
''' # 0: index 1: label
def gen_neomuttrc_accounts(labels):
	with open(L_NEOMUTTRC_ACCOUNTS, 'w') as file:
		file.write(NEOMUTTRC_ACCOUNTS_HEADER)

		write_lines(file, [
			NEOMUTTRC_ACCOUNTS_SOURCE_ENTRY.format(label)
			for label in labels])

		write_lines(file, [
			NEOMUTTRC_ACCOUNTS_FOLDER_HOOK_ENTRY.format(label)
			for label in labels])

		file.write(NEOMUTTRC_ACCOUNTS_NOTMUCH_HEADER)
		file.write('(' + ' or '.join([
			NEOMUTTRC_ACCOUNTS_NOTMUCH_HUB_CONDITION.format(label).strip()
			for label in labels]) + ')')

		file.write(NEOMUTTRC_ACCOUNTS_PAGE_0)
		write_lines(file, [
			NEOMUTTRC_ACCOUNTS_PAGE_ENTRY.format(i, label)
			for (i, label) in enumerate(labels, 1)])
