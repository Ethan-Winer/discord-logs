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
        if thread.id not in self.logs.logs[thread.guild.id].keys():
            await thread.join()
            # print('making new thread file')
            # self.logs.log_new_channel(thread)
            # print('finished new thread file')
            #
            # parent = self.logs.logs[thread.guild.id][thread.parent.id]
            # worksheet = parent['sheet_id']
            # row = parent['row']
            # thread_worksheet = self.logs.logs[thread.guild.id][thread.id]['sheet_id']
            #
            # content = [[
            #     thread.created_at.strftime('%x %X'),
            #     '*Server*',
            #     f'{thread.owner.name} created a new thread {thread_worksheet}',
            # ]]
            # self.logs.update_worksheet(worksheet, row, content)

    async def on_message(self, message):
        self.logs.log_new_message(message)


intents = discord.Intents.all()
client = MyClient(intents)
client.run(os.getenv('test_bot_pog_token'))