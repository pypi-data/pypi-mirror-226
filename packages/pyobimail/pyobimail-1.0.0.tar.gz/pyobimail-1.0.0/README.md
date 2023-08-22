# pyobimail
mail library and bot mail development

# Bot Code Example
```
import os
import pyobimail.utils
from pyobimail.client import EmailBot,EmailMessage


def onenteremail(bot:EmailBot=None,message:EmailMessage=None):
    text = message.mail_content

    reply_subject_text = ''
    reply_subject_file = ''

    if '/start' in text:
        reply = '👋 DeltaFile2Mail 👋\n'
        #message.reply_file(file='logo.png',text=reply,subject=reply_subject_text)
        message.reply_text(text=f'📤Subiendo Archivos...',subject=reply_subject_text)
        pass


def main():
    natcli = EmailBot(email='file2mailbot@gmail.com',email_password='qffvrlcnfhhvjvdi',type='gmail.com')
    natcli.smtp_port=587
    natcli.imap_port=993
    loged = natcli.login()
    if loged:
        print('DeltaFile2Mail Runing!')
        natcli.dispatch_receiv_emails(onenteremail=onenteremail)

if __name__ == '__main__':main()
```
