import os
import discord
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import gspread
from gspread_formatting import set_column_width
import pickle


class Log:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']
        creds = Credentials.from_authorized_user_file('./files/token.json', SCOPES)
        self.drive_client = build('drive', 'v3', credentials=creds)
        self.sheets_client = gspread.oauth(credentials_filename='./files/credentials.json', scopes=SCOPES)

        self.logs = self.__load_logs()

    def __load_logs(self):
        with open('./files/logs.pickle', 'rb') as file:
            out = pickle.load(file)
        return out

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

    # def log(self, message):
    #     if message.guild.id not in self.logs.keys():
    #         body = {
    #             'name': f'{message.guild.name} ({message.guild.id})',
    #             'parents': ['1psHvV-6_U8cgpsF1vlr322aXD9uRnDjp'],
    #             'mimeType': 'application/vnd.google-apps.folder'
    #         }
    #         drive_id = self.drive_client.files().create(body=body).execute()['id']
    #
    #         path = f'./files/logs/{message.guild.id}'
    #         os.makedirs(path)
    #         with open(f'{path}/drive_folder_id.txt', 'w') as file:
    #             file.write(drive_id)
    #         with open(f'{path}/guild_name.txt', 'w') as file:
    #             file.write(message.guild.name)
    #
    #         self.logs[message.guild.id] = {
    #             'drive_folder_id': drive_id,
    #             'guild_name': message.guild.name
    #         }
    #
    #     if message.channel.id not in self.logs[message.guild.id].keys():
    #         name = f'{message.channel.name} ({message.channel.id})'
    #         if type(message.channel) == discord.Thread:
    #             name = f'*thread* {name}'
    #         body = {
    #             'name': name,
    #             'parents': [self.logs[message.guild.id]['drive_folder_id']],
    #             'mimeType': 'application/vnd.google-apps.spreadsheet'
    #         }
    #         sheet_id = self.drive_client.files().create(body=body).execute()['id']
    #         path = f'./files/logs/{message.guild.id}/channels/{message.channel.id}'
    #         os.makedirs(path)
    #
    #         with open(f'{path}/channel_name.txt', 'w') as file:
    #             file.write(message.channel.name)
    #         with open(f'{path}/sheet_id.txt', 'w') as file:
    #             file.write(sheet_id)
    #         with open(f'{path}/row.txt', 'w') as file:
    #             file.write('0')
    #
    #         self.logs[message.guild.id][message.channel.id] = {
    #             'name': message.channel.name,
    #             'sheet_id': sheet_id,
    #             'row': 1
    #         }
    #         sheet = self.sheets_client.open_by_key(sheet_id).sheet1
    #         self.__make_first_row(sheet)
    #     channel = self.logs[message.guild.id][message.channel.id]
    #     sheet = self.sheets_client.open_by_key(channel['sheet_id']).sheet1
    #     channel['row'] += 1
    #     sheet.resize(channel['row'], 6)  # temporary
    #
    #     files = ''
    #     if len(message.attachments) > 0:
    #         for file in message.attachments:
    #             files += file.url + '\n'
    #
    #     content = [[
    #         message.created_at.strftime('%x %X'),
    #         f'Username: {message.author.name}\nNickname: {message.author.display_name}',
    #         message.content,
    #         files,
    #         str(message.author.id),
    #         str(message.id)
    #     ]]
    #     sheet.update(f'A{channel["row"]}', content)
    def __log_new_guild(self, guild):
        body = {
            'name': f'{guild.name} ({guild.id})',
            'parents': ['1psHvV-6_U8cgpsF1vlr322aXD9uRnDjp'],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        drive_id = self.drive_client.files().create(body=body).execute()['id']

        self.logs[guild.id] = {
            'drive_folder_id': drive_id,
            'guild_name': guild.name
        }

    def log_new_channel(self, channel):
        isChannel = type(channel) == discord.TextChannel
        guild = channel.guild
        name = f'{channel.name} ({channel.id})'
        if isChannel:
            name = f'-Channel- {name}'
        else:
            name = f'#Thread# {name}'
        body = {
            'name': name,
            'parents': [self.logs[guild.id]['drive_folder_id']],
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        sheet_id = self.drive_client.files().create(body=body).execute()['id']
        sheet = self.sheets_client.open_by_key(sheet_id)

        self.logs[guild.id][channel.id] = {
            'name': channel.name,
            'sheet_id': sheet_id,
            'row': 1
        }
        if isChannel:
            self.logs[guild.id][channel.id]['thread_count'] = 0

        worksheet = sheet.sheet1
        worksheet.resize(rows=2, cols=6)
        worksheet.update('A1', [['Date', 'Author', 'Message', 'Attached Files', 'Author ID', 'Message ID']])
        worksheet.freeze(rows='1')
        worksheet.format('A:F', {'verticalAlignment': 'TOP'})
        worksheet.format('C', {'wrapStrategy': 'WRAP'})
        set_column_width(worksheet, 'A', 135)
        set_column_width(worksheet, 'B', 200)
        set_column_width(worksheet, 'C', 400)
        set_column_width(worksheet, 'E:F', 135)

        if isChannel:
            sheet.add_worksheet(title='Threads', rows=100, cols=4)

    def log_new_message(self, message):
        if message.guild.id not in self.logs.keys():
            self.__log_new_guild(message.guild)
        if message.channel.id not in self.logs[message.guild.id].keys():
            self.log_new_channel(message.channel)

        channel = self.logs[message.guild.id][message.channel.id]
        sheet = self.sheets_client.open_by_key(channel['sheet_id']).sheet1
        channel['row'] += 1
        sheet.resize(channel['row'], 6)  # temporary
        content = []
        match message.type:
            case discord.MessageType.default:
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
        self.update_worksheet(sheet, channel['row'], content)

    def update_worksheet(self, worksheet, row, content):
        worksheet.update(f'A{row}', content)