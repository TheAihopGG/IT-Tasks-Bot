import disnake
import random
import services.api as api
from services.embeds import *
from services.typed_dicts import TypedTask
from disnake.ext import commands

class MemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot, /):
        super().__init__()
        self.bot = bot

    @commands.slash_command(name='random-task')
    async def get_random_task(self, inter: disnake.ApplicationCommandInteraction):
        tasks_ids = api.get_tasks_ids()

        if tasks_ids:
            task: TypedTask = api.get_task(random.choice(tasks_ids))
            embed = Info()
            embed.add_field(task['title'], task['text'])
            await inter.response.send_message(embed=embed)
        else:
            await inter.response.send_message(embed=Error(description='No tasks available'))


def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))
