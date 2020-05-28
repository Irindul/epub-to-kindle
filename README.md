# Epub to Mobi to Kindle :smile: 

> This was only tested on macOS but should work on Linux as well, provided you installed the `ebook-convert` properly

## Prerequisites

You must install the `ebook-convert` tool from the [calibre](https://calibre-ebook.com/) applications. 

> on macOS, if you did not set up the application in the default folder, you need to provide the path to the script using an argument as described below

## Configuration


This is a simple set of scripts to convert `.epub` to `.mobi` and send them by mail using a Gmail account.

The mail configuration must be created in an `env` file which could look like so: 
```bash 
export KINDLE_MAIL_ADDR="yourmail@domain.com"
export KINDLE_MAIL_PWD="yourpasswd"
export KINDLE_MAIL_TO="youkindlemail@kindle.com"
```

> If you have 2FA activated, you need to create an [App password](https://support.google.com/accounts/answer/185833?hl=en), or disable 2FA but I don't recommend doing this

> If you don't have 2FA activated, well.. you should :')

This file will be sourced by the `convert_and_send.sh` so that the credentials are not in the code nor in the bash HISTORY.

Then, all you need to do, is execute the `convert_and_send.sh` script :

```bash
chmod +x convert_and_send.sh
./convert_and_send.sh
```

## Conversion

For the conversion, I used the `ebook-convert` command of the calibre app. The script `convert_epub_to_mobi.py` will simply get all files of the folder `Epubs/` and convert them to mobi in the `Mobi/` folder.  The folder `Epubs/` is deleted at the end. 

> The files must have an `.epub` extension or the script will skip them

The python script supports different options : 
- `-c/--converter` to specify the path to the `ebook-convert` tool for non-standard installation
- `-e/--epubs` to specify input folder for the epubs
- `-m/--mobis` to specify output folder for converted mobis  

## Email 

The script `send_to_kindle.py` will get all files of the `Mobi/` folder, and build them as MIME parts using the `smtplib` python library (_it should be available without needing pip_). 

## TO DO 

- ~~[x] Better error handling~~

- ~~[x] Convert `convert_epub_to_mobi.sh` to Python~~
- ~~[x] Add directories (epub, mobi) as arguments to the script~~
- [ ] Add support for `dotenv` library
- [ ] Add directories as arguments in `send_to_kindle.py`
- [ ] Check if the ebook-converter tool is properly installed
- [ ] Test on Linux