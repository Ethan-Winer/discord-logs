import discord
import os
import discord_log


class MyClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.logs = discord_log.Log()

    async def on_ready(self):
        print('Logged in as', self.user)

    # async def on_thread_delete(self, thread):
    #     print('rip thread')
    #
    # async def on_thread_update(self, before, after):
    #     if after.archived == True:
    #         print('archived')
    #
    async def on_thread_join(self, thread):
        await thread.join()



    async def on_message(self, message):
        self.logs.log(message)


intents = discord.Intents.all()
client = MyClient(intents)
client.run(os.getenv('test_bot_pog_token'))
