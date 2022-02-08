#!/usr/bin/env python3
import os
import smtplib
import subprocess
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import listdir
from os.path import isfile, join


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


wanted_ext = '.mobi'


def print_progress(msg):
    print(f'[{bcolors.WARNING}*{bcolors.ENDC}] - {msg}')


def print_success(msg):
    print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] - {msg}')


def print_error(msg):
    sys.stderr.write(f'[{bcolors.FAIL}x{bcolors.ENDC}] - {msg}')
    exit(1)


def check_env(env):
    if env not in os.environ:
        print_error(f'you need to set the {env} variable')


def is_wanted_ext(path):
    _, ext = os.path.splitext(path)
    return ext == wanted_ext


# Ensuring env variables are properly set
check_env("KINDLE_MAIL_ADDR")
check_env("KINDLE_MAIL_PWD")
check_env("KINDLE_MAIL_TO")

from_addr = os.getenv('KINDLE_MAIL_ADDR')
pwd = os.getenv('KINDLE_MAIL_PWD')
to_addr = os.getenv('KINDLE_MAIL_TO')

# Setting different paths
cwd = os.getcwd()
epubs_path = f'{cwd}/Mobi'

# Crafting mail
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = "New Ebooks"
msg.attach(MIMEText("New books coming up!", 'plain'))

# Listing wanted files (.epub)
books = [f for f in listdir(epubs_path) if isfile(
    join(epubs_path, f)) and is_wanted_ext(f)]

if len(books) == 0:
    print
    exit(0)

for book in books:
    _, ext = os.path.splitext(book)

    print_progress(f'building attachment for {book}')
    book_path = f'{epubs_path}/{book}'

    with open(book_path, 'rb') as attachment:
        p = MIMEBase('application', 'octet-stream')
        p.set_payload(attachment.read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename= {book}')
        msg.attach(p)

    print_progress('deleting file...')
    #os.remove(book_path)

# converting the message as text
text = msg.as_string()


print_progress(f'logging in to {from_addr} account')
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(from_addr, pwd)

print_success(f'successful login')

print_progress(f'sending mail to {to_addr}')

s.sendmail(from_addr, to_addr, text)
print_success('Sent :D')

# Freeing memory
s.quit()
