import discord
import os
import discord_log

logs = discord_log.Log()

class MyClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        print('Logged on as', self.user)
        # self.intents.guilds = True
        # self.intents.messages = True


    async def on_thread_join(self, thread):
        print('new thread')
        await thread.join()

    async def on_message(self, message):
        logs.log(message)


intents = discord.Intents.all()
client = MyClient(intents)
client.run(os.getenv('test_bot_pog_token'))
