from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

folderId = '1psHvV-6_U8cgpsF1vlr322aXD9uRnDjp'

def main():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    service = build('drive', 'v3', credentials=creds)
    result = service.files().list(q= "'"+folderId +"' in parents").execute()
    for a in result['files']:
        print(a)

if __name__ == '__main__':
    main()