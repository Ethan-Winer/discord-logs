import discord
import os
import gspread

import discord_log
from discord_log import log
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = Credentials.from_authorized_user_file('./files/token.json', SCOPES)

drive_client = build('drive', 'v3', credentials=creds)
sheets_client = gspread.oauth(credentials_filename='./files/credentials.json', scopes=SCOPES)

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        log(message, drive_client, sheets_client)

        if message.content == 'ping':
            await message.channel.send('pong')

# intents = discord.Intents.default()
# intents.message_content = True


client = MyClient()
client.run(os.getenv('test_bot_pog_token'))
