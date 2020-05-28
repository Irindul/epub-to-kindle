#!/usr/bin/env python3
import argparse
import glob
import os
import shlex
import subprocess
import sys

from sys import platform
from os import path as ospath
from os import walk

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_progress(msg):
    print(f'[{bcolors.WARNING}*{bcolors.ENDC}] - {msg}')


def print_success(msg):
    print(f'[{bcolors.OKGREEN}+{bcolors.ENDC}] - {msg}')


def print_error(msg):
    sys.stderr.write(f'[{bcolors.FAIL}x{bcolors.ENDC}] - {msg}')
    exit(1)


def has_trailing_slash(path: str):
    return path[-1] == "/"

def check_path_exists(path: str):
    if not ospath.exists(path):
        print_error(f'{path} does not exists or is not a folder, please provide a valid path')

def trim_path_to_title(path: str) -> str:
    return ospath.splitext(ospath.basename(file))[0]

def convert_to_epub(file: str, converter: str, dst: str):
    if ".epub" not in file: 
        print_progress(f'Skipping {file} as the extension is not .epub')
        return
    
    title = trim_path_to_title(file)
    print_progress(f'converting {title}.epub...')
    converted = f'{dst}{title}.mobi'
    child = subprocess.run([converter, file, converted],  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if child.returncode != 0:
        print_error(child.stderr)
    else: 
        print_success(f'conversion successfull for {title}.epub')
        os.remove(file)
        print_success(f'file {title}.epub deleted')

# Setting up the CLI arguments
cwd = os.getcwd()
parser = argparse.ArgumentParser(description="Convert .epub files to .mobi")
parser.add_argument('-c', 
                    '--converter',
                    action="store",
                    dest="converter",
                    default="",
                    help="Use this to replace the path of ebook-converter tool"
                    )
parser.add_argument('-e',
                    '--epubs',
                    action="store",
                    dest="epubs",
                    default=f"{cwd}/Epubs/",
                    help="Path to the source for epubs"
                    )
parser.add_argument('-m',
                    '--mobis',
                    action="store",
                    dest="mobis",
                    default=f"{cwd}/Mobi/",
                    help="Path to the destination for mobi-converted tool"
                    )
args = parser.parse_args()

if args.converter != "":
    converter = args.converter
elif platform == "darwin":
    converter = "/Applications/calibre.app/Contents/MacOS/ebook-convert"
else: 
    converter = subprocess.run(['which', "ebook-converter"], stdout=subprocess.PIPE).stdout


epubs = args.epubs if has_trailing_slash(args.epubs) else f"{args.epubs}/"
mobis = args.mobis if has_trailing_slash(args.mobis) else f"{args.mobis}/"

check_path_exists(epubs)
check_path_exists(mobis)

pattern_matching = f'{epubs}*.epub'
for file in glob.glob(pattern_matching):
    convert_to_epub(file, converter, mobis)