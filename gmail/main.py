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
    msgData = service.users().messages().list(userId='me').execute()['messages']
    idList = []
    for i in range(len(msgData)):
        idList.append(msgData[i]['id'])
    print(len(idList))
    msg = service.users().messages().get(id=message_id,userId='me', format='raw').execute()
    msg_str = base64.urlsafe_b64decode(msg['raw'])
    # print(msg_str)
    email_msg = email.message_from_bytes(msg_str)
    body=None
    html=''

    email_subject = email_msg.get_all('Subject')
    from_sender = email_msg.get_all('From')
    to_recipient = email_msg.get_all('To')
    return_path = email_msg.get_all('Return-Path')
    delivered_to = email_msg.get_all('Delivered-To')
    datetime_rx = email_msg.get_all('Date')

    print(email_subject)

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
    body = re.sub(r'\n\s*\n', '\n\n',body)
    print(body)



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
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        get_email_data(service,'186064f58a574920')
        print('################################################################################################')
        get_email_data(service,'185fc4fa5d982eda')
        print('################################################################################################')
        get_email_data(service,'185f29195ee26c4b')
        return
        results = service.users().labels().list(userId='me').execute()
        print(results)

        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        print(labels)
        # for label in labels:
            # print(type(label))
            # print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()



"""
dict_keys(['id', 'threadId', 'labelIds', 'snippet', 'payload', 'sizeEstimate', 'historyId', 'internalDate'])
payload: dict_keys(['partId', 'mimeType', 'filename', 'headers', 'body'])
"""