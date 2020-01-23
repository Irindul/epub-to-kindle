#!/usr/bin/env python3
import os
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import listdir
from os.path import isfile, join

def check_env(env):
    if env not in os.environ:
        print(f'You need to set the {env} variable')
        exit(1)

def is_wanted_ext(path):
    _, ext = os.path.splitext(path)
    return ext == wanted_ext


check_env("KINDLE_MAIL_ADDR")
check_env("KINDLE_MAIL_PWD")
check_env("KINDLE_MAIL_TO")

from_addr = os.getenv('KINDLE_MAIL_ADDR')
pwd = os.getenv('KINDLE_MAIL_PWD')
to_addr = os.getenv('KINDLE_MAIL_TO')

cwd = os.getcwd()
epubs_path = f'{cwd}/Mobi'
wanted_ext = '.mobi'
from_addr = os.getenv("KINDLE_MAIL_ADDR")
to_addr = "mathieu.regnard2@gmail.com"
converter_sh = f'{cwd}/convert_epub_to_mobi.sh'

rc = subprocess.call(converter_sh)
if rc != 0:
    exit(rc)

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = "New Ebooks"

body = "New books coming up!"

msg.attach(MIMEText(body, 'plain'))
books = [f for f in listdir(epubs_path) if isfile(join(epubs_path, f)) and is_wanted_ext(f) ]

if len(books) == 0:
    print('Hey! There is no epub in that folder :\'(')
    exit(0)

for book in books:
    _, ext = os.path.splitext(book)
    if ext != wanted_ext:
        print(f'Skipping {book} for there is no .epub extension')
        continue

    print(f'Building attachment for {book}')

    book_path = f'{epubs_path}/{book}'
    with open(book_path, 'rb') as attachment:
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename= {book}')
        msg.attach(p)

    print('Deleting file...')
    os.remove(book_path)


s = smtplib.SMTP('smtp.gmail.com', 587)

print("Logging in to GMAIL")
s.starttls()
s.login(from_addr, pwd)

text = msg.as_string()

print(f'Sending mail to {to_addr}')

s.sendmail(from_addr, to_addr, text)
print('[*] Sent :D')
s.quit()
