# Epub to Mobi to Kindle :smile: 

> This only works on macOS for now and I will try to generify it for other OS if I ever find the time...


This is a simple set of scripts to convert `.epub` to `.mobi` and send them by mail using a Gmail account.

The mail configuration must be created in an `env` file which could look like so: 
```bash 
export KINDLE_MAIL_ADDR="yourmail@domain.com"
export KINDLE_MAIL_PWD="yourpasswd"
export KINDLE_MAIL_TO="youkindlemail@kindle.com"
```

This file will be sourced by the `convert_and_send.sh` so that the credentials are not in the code

Then, all you need to do, is execute the `convert_and_send.sh` script :

```bash
chmod +x convert_and_send.sh
./convert_and_send.sh
```

## Conversion

For the conversion, I used the `ebook-convert` command of the calibre app. The script `convert_epub_to_mobi.sh` will simply get all files of the folder `Epubs/` and convert them to mobi in the `Mobi/` folder.  The folder `Epubs/` is deleted at the end. 

> I did not handle any case where the file are not `.epub`, so be careful, or PR me ;) 

## Email 

The script `send_to_kindle.py` will get all files of the `Mobi/` folder, and build them as MIME parts using the `smtplib` python library (_it should be available without needing pip_). 

> If you have 2FA activated, you need to create an [App password](https://support.google.com/accounts/answer/185833?hl=en), or disable 2FA but I don't recommend doing this

> If you don't have 2FA activated, well you should :')


I used Python for this part because it was getting a bit of a hassle with bash and the `mail` command to send multiple attachments.


## TO DO 

- [x] Better error handling
- [ ] Check for existing file for renaming
- [ ] Add support for `dotenv` library
- [x] Convert `convert_epub_to_mobi.sh` to Python
- [x] Add directories (epub, mobi) as arguments to the script
