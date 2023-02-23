from __future__ import print_function

import os.path
import base64
import email
import html.parser
import re
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import pandas as pd
from flask import Flask,request
import datetime,time

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/fetch_user_token", methods=['POST'])
def fetch_user_token():
    try:
        # extract jwt token from request header - x-auth-token
        # extract user email from jwt token
        # Api Call 1 
        user_token = request.headers.get('x-auth-token')

        user_micro_svc_url = "http://localhost:3000/api/user/user_data"

        payload={}
        headers = {
        'x-auth-token': user_token
        }

        response = requests.request("POST",user_micro_svc_url, headers=headers, data=payload)

        response = json.loads(response.text)
        print(type(response))
        data = response['user_data']['Gmail_Access']
        data['client_id'] = '564790885481-7d0fdgi7jirh5mke5u4r3v2dqvbj8ba9.apps.googleusercontent.com'
        data['client_secret'] = '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'
        data.pop('expiry_date')
        #print(data)
        #  write respone data as json file
        user_id = response['user_data']['_id']
        print(response['user_data']['last_scan_timestamp'])
        
        last_timestamp = response['user_data']['last_scan_timestamp']
        
        file_pth = f'{str(user_id)}.json'
        with open(f'{str(user_id)}.json', 'w') as outfile:
            json.dump(data, outfile)
        last_timeStamp = fetch_mails(file_pth,last_timestamp)
        if last_timeStamp == None:
            last_timeStamp = last_timestamp
            
        # Api Call 2 -- Update last_scan_timestamp
        url = "http://localhost:3000/api/user/update_last_scan_time"

        payload = json.dumps({
        "last_scan_time": last_timeStamp
        })
        headers = {
        'Content-Type': 'application/json',
        'x-auth-token': user_token
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        ### RETURN RESPONSE
        return {
            "status": "success",
            "message": "Mails Succssfully Scaned",
            "code": 200
        }

    except Exception as e:
        print(e)
        return {
            "status": "error",
            "message": "Error while fetching user token",
            "code": 500
        }




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



def fetch_mails(file_pth,last_timestamp):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(file_pth):
        creds = Credentials.from_authorized_user_file(file_pth, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(file_pth, 'w') as token:
            token.write(creds.to_json())

    try:
        m2int = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12
        }
        service = build('gmail', 'v1', credentials=creds)
        res = service.users().messages().list(userId='me',maxResults=50,q=f'after:{last_timestamp}',labelIds='INBOX').execute()
   
        senderList = []
        bodyList = []
        subjectList = []
        dateTimeList = []
        msgIdList = []
        for msg in res['messages']:
            sender, subject, body, dateTime = get_email_data(service, msg['id'])            
            body = cleanBody(body)                     
            senderList.append(sender)
            bodyList.append(body)
            subjectList.append(subject)
            dateTimeList.append(dateTime)
            msgIdList.append(msg['id'])
        
        df = pd.DataFrame(list(zip(msgIdList, senderList, subjectList, bodyList, dateTimeList)))    
        print(df.head()[3])
        
        #print(df[4].iloc[0])
        last_date = df[4].iloc[0]
        last_date = last_date[0]
        last_date = last_date.split(',')
        last_date = last_date[1].strip().split(' ')
        last_date_day = last_date[0]
        last_date_month = last_date[1]
        last_date_month = m2int[last_date_month]
        last_date_year = last_date[2]
        last_date_h = last_date[3].split(':')
        last_date_hr = last_date_h[0]
        last_date_min = last_date_h[1]
        last_date_sec = last_date_h[2]
        # convert to unix timestamp
        last_date = datetime.datetime(int(last_date_year), int(last_date_month), int(last_date_day), int(last_date_hr), int(last_date_min), int(last_date_sec))
        last_date = time.mktime(last_date.timetuple())
        last_time_stamp = str(last_date).split('.')
        df.to_csv('email.csv', index=False, header=False)
        return last_time_stamp[0]

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def cleanBody(body):
    body = re.sub('{.*.}','',body,flags=re.S)
    body = re.sub('http\S+\s*', ' ', body)  # remove URLs
    body = re.sub('RT|cc', ' ', body)  # remove RT and cc
    body = re.sub('#\S+', '', body)  # remove hashtags
    body = re.sub('@\S+', '  ', body)  # remove mentions    
    body = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-/;<=>?@[\]^_`{|}~"""), ' ', body)  # remove punctuations
    body = re.sub(r'[^\x00-\x7f]', r' ', body)
    body = re.sub('\s+', ' ', body)  # remove extra whitespace
    return body   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)