from __future__ import print_function


from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import gspread

from time import sleep

SCOPES = ['https://www.googleapis.com/auth/drive']

folderId = '1psHvV-6_U8cgpsF1vlr322aXD9uRnDjp'

def main():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # driveService = build('drive', 'v3', credentials=creds)

    sheetKey = '1OTcop7fTCNYQ5XfmdfVnr9KjDUA1Xv53G2aGkS0BYYE'

    gc = gspread.oauth(credentials_filename='credentials.json', scopes=SCOPES)
    sh = gc.open_by_key(sheetKey).sheet1
    sh.update('A2', 'more text')
    # result = driveService.files().list(q= "'"+folderId +"' in parents").execute()
    # body = {
    #     'name': 'bruhbruh19',
    #     'parents': [folderId],
    #     'mimeType': 'application/vnd.google-apps.spreadsheet'
    # }
    # file = driveService.files().create(body=body).execute()


if __name__ == '__main__':
    main()
