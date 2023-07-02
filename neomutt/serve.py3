import http.server
import socketserver
import subprocess
import sys
import os
import yaml

import re
import json
import datetime

C_SERVERC = sys.argv[1]

def filename_string(string):
	lowercase_string = string.lower()
	alphanumeric_string = re.sub(r'\W+', '', lowercase_string)
	return alphanumeric_string.replace(' ', '_')

class MaildirMessage:
	def __init__(self, received_time, sender, to, subject, content):
		self.received_time = received_time
		self.sender = sender
		self.to = to
		self.subject = subject
		self.content = content
		self.filename = f'{self.received_time.timestamp()}_{filename_string(sender)}_{filename_string(subject)}'

	def write_in_maildir(self, maildir_path):
		message_path = os.path.expanduser(f'{maildir_path}/cur/{self.filename}')
		with open(message_path, 'w') as file:
			mbox_date = self.received_time.strftime('%a %b %d %H:%M:%S %Y')
			file.write(
				f'From MAILDIR-SERVICE {mbox_date}\n'
				f'From: {self.sender} <{filename_string(self.sender)}@maildir>\n'
				f'To: {self.to}\n'
				f'Subject: {self.subject}\n'
				f'Date: {mbox_date}\n\n'
				f'{self.content}\n\n')

# Parse generated configuration file
with open(C_SERVERC, 'r') as config_yaml:
	config = yaml.safe_load(config_yaml)

# Create maildirs
for (label, maildir) in config['accounts'].items():
	os.makedirs(f'{maildir}/cur', exist_ok=True)
	os.makedirs(f'{maildir}/new', exist_ok=True)
	os.makedirs(f'{maildir}/tmp', exist_ok=True)

def handle_notmuch_new(req):
	cmd = ['/usr/bin/notmuch', 'new', '--verbose', '2>&1',
		'>', '/notmuch.log']
	output = subprocess.check_output(cmd)
	return (200, output.decode())

def handle_vdirsyncer_discover(req):
	cmd = ['yes', '|', 'vdirsyncer', 'discover', '2>&1', '>', '/vdirsyncer.log']
	output = subprocess.check_output(cmd)
	return (200, output.decode())

def handle_vdirsyncer_sync(req):
	cmd = ['vdirsyncer', 'sync', '2>&1', '>', '/vdirsyncer.log']
	output = subprocess.check_output(cmd)
	return (200, output.decode())

def handle_maildir_add(req):

	# Parse request and check account
	msg_json = json.loads(req)
	if msg_json['account'] not in config['accounts'].keys():
		return (404, "No such account")

	# Generate message in mail format
	msg = MaildirMessage(datetime.datetime.now(),
		msg_json['sender'], msg_json['to'], msg_json['subject'],
		msg_json['body'])

	# Write into maildir
	maildir = config['accounts'][msg_json['account']]
	msg.write_in_maildir(maildir)

	return (200, "Inserted 1 message\n")

commands = {
	'mail-update': handle_notmuch_new,
	'mail-add': handle_maildir_add
	'webdav-discover': handle_vdirsyncer_discover,
	'webdav-sync': handle_vdirsyncer_sync,
}

class RequestHandler(http.server.SimpleHTTPRequestHandler):
	def do_POST(self):
		# Strip leading /
		command = self.path[1:]
		if command in commands:
			try:
				content_length = int(self.headers['Content-Length'])
				post_data = self.rfile.read(content_length)
				(code, output) = commands[command](post_data)
			
			except Exception as e:
				code = 500
				output = str(e)

			print(code)
			print(output)

		else:
			code = 404
			output = 'Invalid endpoint\n'

		self.send_response(code)
		self.send_header('Content-type', 'text/plain')
		self.end_headers()
		self.wfile.write(output.encode())

# Set up the server
PORT = 4000
handler = RequestHandler
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), handler)

# Start the server
print(f"Server listening on internal port {PORT}")
httpd.serve_forever()
