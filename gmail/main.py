from __future__ import print_function

import os.path
import base64
import email
import html.parser
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd

class HTMLTextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super(HTMLTextExtractor, self).__init__()
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def get_text(self):
        return ''.join(self.result)

def html_to_text(html):
    s = HTMLTextExtractor()
    s.feed(html)
    return s.get_text()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_email_data(service, message_id):
    msg = service.users().messages().get(id=message_id,userId='me', format='raw').execute()
    msg_str = base64.urlsafe_b64decode(msg['raw'])    
    email_msg = email.message_from_bytes(msg_str)    
    body=None
    html=''

    email_subject = email_msg.get_all('Subject')
    from_sender = email_msg.get_all('From')
    datetime_rx = email_msg.get_all('Date')    

    if email_msg.is_multipart():
        for part in email_msg.walk():
            content_type = part.get_content_type()
            disp = str(part.get('Content-Disposition'))
            # look for plain text parts, but skip attachments
            if part.get_content_charset() is None:
                # We cannot know the character set, so return decoded "something"
                body = part.get_payload(decode=True)
                continue
            if content_type == 'text/plain' and 'attachment' not in disp:
                charset = part.get_content_charset()
                # decode the base64 unicode bytestring into plain text
                body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                # if we've found the plain/text part, stop looping thru the parts
                break
            if content_type == 'text/html' and 'attachment' not in disp:
                charset = part.get_content_charset()
                html = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                # if we've found the plain/text part, stop looping thru the parts
                break           
    else:
        # not multipart - i.e. plain text, no attachments
        content_type = email_msg.get_content_type()
        if email_msg.get_content_charset() is None:
            # We cannot know the character set, so return decoded "something"
            body = email_msg.get_payload(decode=True)
        else: 
            charset = email_msg.get_content_charset()
            if content_type == 'text/plain':
                body = email_msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
            if content_type == 'text/html':
                html = email_msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
    if body is not None:
        body = body.strip()
    else:
        body  = html_to_text(html)
        body = body.strip()
    body = re.sub(r'\n\s*\n', '\n\n',str(body))
    return from_sender, email_subject, body, datetime_rx



def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        res = service.users().messages().list(userId='me',maxResults=50,q='after:2022/01/01').execute()
   
        senderList = []
        bodyList = []
        subjectList = []
        dateTimeList = []
        msgIdList = []
        for msg in res['messages']:
            sender, subject, body, dateTime = get_email_data(service, msg['id'])            
            body = removeCSS(body)                     
            senderList.append(sender)
            bodyList.append(body)
            subjectList.append(subject)
            dateTimeList.append(dateTime)
            msgIdList.append(msg['id'])
        
        df = pd.DataFrame(list(zip(msgIdList, senderList, subjectList, bodyList, dateTimeList)))        

    except HttpError as error:
        print(f'An error occurred: {error}')


def removeCSS(body):
    return re.sub('{.*.}','',body,flags=re.S)    

if __name__ == '__main__':
    main()

