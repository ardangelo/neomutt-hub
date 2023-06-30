from config.defs import *

MAILCAPRC_BODY = f'''
text/html; w3m -I %{{charset}} -T text/html; copiousoutput;
text/plain; less
'''
def gen_mailcaprc():
	with open(L_MAILCAPRC, 'w') as file:
		file.write(MAILCAPRC_BODY)
