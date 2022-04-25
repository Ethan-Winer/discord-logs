import discord
import os
import discord_log
from pprint import pprint

class MyClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.logs = discord_log.Log()

    async def on_ready(self):
        print('Logged in as', self.user)

    async def on_thread_delete(self, thread):
        print('rip thread')

    async def on_thread_join(self, thread):
        await thread.join()
        print('thread join')

    async def on_message(self, message):
        # self.logs.log(message)
        # print(type(message.channel) == discord.Thread)
        return
intents = discord.Intents.all()
client = MyClient(intents)
client.run(os.getenv('test_bot_pog_token'))
