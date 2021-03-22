#!/usr/bin/eval python
import sys
import configparser
import imaplib
import base64
import os
import email
import pdb
from datetime import datetime
import re


# function to decode email subject
import base64, quopri
def encoded_words_to_text(encoded_words):
    encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
    charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
    if encoding == 'B':
        byte_string = base64.b64decode(encoded_text)
    elif encoding == 'Q':
        byte_string = quopri.decodestring(encoded_text)
    return byte_string.decode(charset)


# get arguments
config_file = sys.argv[1]
output_dir = sys.argv[2]

# get config
config = configparser.ConfigParser()
config.read(config_file)
user = config.get('gmail', 'user')
password = config.get('gmail', 'password')
gmail_search = config.get('gmail', 'search_string')

# open mail
mail = imaplib.IMAP4_SSL('imap.gmail.com', '993')
mail.login(user, password)
mail.select('Inbox')

# search for invoice emails
status, data = mail.search(None, 'X-GM-RAW', gmail_search)
mail_ids = data[0]

# loop over the emails
for i,mail_id in enumerate(mail_ids.split()):

    # fetch the mail
    mail_status, mail_data = mail.fetch(mail_id, '(RFC822)' )
    raw_email = mail_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    #pdb.set_trace()


    # downloading attachments (from https://medium.com/@sdoshi579/to-read-emails-and-download-attachments-in-python-6d7d6b60269)
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):

            # debug
            #if i == 70:
            #    pdb.set_trace()

            # get date
            mail_date = datetime.strptime(email_message['Date'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')

            # get subject
            if email_message['Subject'].strip().startswith('=?'):
                mail_subject = encoded_words_to_text(email_message['Subject'].strip())
            else:
                mail_subject = email_message['Subject'].strip()

            # decode fileName if needed
            fileName = fileName.strip()
            if fileName.startswith('=?'):
                fileName = encoded_words_to_text(fileName)

            filePath = os.path.join(output_dir, f"{mail_date}__{mail_subject}__{fileName}")
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
            print(f"Saved file #{i}, {filePath}")








