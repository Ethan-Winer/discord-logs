import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import gspread
from gspread_formatting import set_column_width
class Log:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = Credentials.from_authorized_user_file('./files/token.json', SCOPES)
        self.drive_client = build('drive', 'v3', credentials=creds)
        self.sheets_client = gspread.oauth(credentials_filename='./files/credentials.json', scopes=SCOPES)

        self.logs = self.__load_logs()

    def __load_logs(self):
        logs = {}
        for guild_id in os.listdir('./files/logs'):

            path = f'./files/logs/{guild_id}'
            guild_id = int(guild_id)
            logs[guild_id] = {}

            with open(f'{path}/guild_name.txt', 'r') as guild_name:
                logs[guild_id]['guild_name'] = guild_name.read()
            with open(f'{path}/drive_folder_id.txt', 'r') as drive_folder_id:
                logs[guild_id]['drive_folder_id'] = drive_folder_id.read()

            path = f'{path}/channels'
            for channel_id in os.listdir(path):
                path = f'./files/logs/{guild_id}/channels/{channel_id}'
                channel_id = int(channel_id)
                logs[guild_id][channel_id] = {}

                with open(f'{path}/channel_name.txt', 'r') as channel_name:
                    logs[guild_id][channel_id]['name'] = channel_name.read()
                with open(f'{path}/sheet_id.txt', 'r') as sheet_id:
                    logs[guild_id][channel_id]['sheet_id'] = sheet_id.read()
                sheet_id = logs[guild_id][channel_id]['sheet_id']
                logs[guild_id][channel_id]['row'] = self.sheets_client.open_by_key(sheet_id).sheet1.row_count
        return logs


    def __make_first_row(self, sheet):
        sheet.resize(rows=2, cols=6)
        sheet.update('A1', [['Date', 'Author', 'Message', 'Attached Files', 'Author ID', 'Message ID']])
        sheet.freeze(rows='1')
        sheet.format('A:F', {'verticalAlignment': 'TOP'})
        sheet.format('C', {'wrapStrategy': 'WRAP'})
        set_column_width(sheet, 'A', 135)
        set_column_width(sheet, 'B', 200)
        set_column_width(sheet, 'C', 400)
        set_column_width(sheet, 'E:F', 135)

    def log(self, message):
        if message.guild.id not in self.logs.keys():
            body = {
                'name': f'{message.guild.name} ({message.guild.id})',
                'parents': ['1psHvV-6_U8cgpsF1vlr322aXD9uRnDjp'],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            drive_id = self.drive_client.files().create(body=body).execute()['id']

            path = f'./files/logs/{message.guild.id}'
            os.makedirs(path)
            with open(f'{path}/drive_folder_id.txt', 'w') as file:
                file.write(drive_id)
            with open(f'{path}/guild_name.txt', 'w') as file:
                file.write(message.guild.name)

            self.logs[message.guild.id] = {
                'drive_folder_id': drive_id,
                'guild_name': message.guild.name
            }

        if message.channel.id not in self.logs[message.guild.id].keys():
            body = {
                'name': f'{message.channel.name} ({message.channel.id})',
                'parents': [self.logs[message.guild.id]['drive_folder_id']],
                'mimeType': 'application/vnd.google-apps.spreadsheet'
            }
            sheet_id = self.drive_client.files().create(body=body).execute()['id']
            path = f'./files/logs/{message.guild.id}/channels/{message.channel.id}'
            os.makedirs(path)

            with open(f'{path}/channel_name.txt', 'w') as file:
                file.write(message.channel.name)
            with open(f'{path}/sheet_id.txt', 'w') as file:
                file.write(sheet_id)
            with open(f'{path}/row.txt', 'w') as file:
                file.write('0')

            self.logs[message.guild.id][message.channel.id] = {
                'name': message.channel.name,
                'sheet_id': sheet_id,
                'row': 1
            }
            sheet = self.sheets_client.open_by_key(sheet_id).sheet1
            self.__make_first_row(sheet)
        channel = self.logs[message.guild.id][message.channel.id]
        sheet = self.sheets_client.open_by_key(channel['sheet_id']).sheet1
        channel['row'] += 1
        sheet.resize(channel['row'], 6)     # temporary

        files = ''
        if len(message.attachments) > 0:
            for file in message.attachments:
                files += file.url + '\n'

        content = [[
            message.created_at.strftime('%x %X'),
            f'Username: {message.author.name}\nNickname: {message.author.display_name}',
            message.content,
            files,
            str(message.author.id),
            str(message.id)
        ]]
        sheet.update(f'A{channel["row"]}', content)