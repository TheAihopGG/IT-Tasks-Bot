import json
import disnake
import random
import requests
from data.settings import API_URL
from services.embeds import *
from services.typed_dicts import TypedTask
from disnake.ext import commands

class MemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot, /):
        super().__init__()
        self.bot = bot

    @commands.slash_command(name='random-task', description='Returns random task')
    async def get_random_task(self, inter: disnake.ApplicationCommandInteraction):
        response = requests.get(f'{API_URL}/tasks/ids')
        match response.status_code:
            case 200:
                tasks_ids: list[int] = json.loads(response.content.decode())['ids']
                response = requests.get(f'{API_URL}/task/?id={random.choice(tasks_ids)}')
                match response.status_code:
                    case 200:
                        task: TypedTask = json.loads(response.content.decode())['task']
                        await self.send_task(inter, task)
                    
                    case _:
                        await inter.response.send_message(embed=Error(description=response.content))
            
            case _:
                await inter.response.send_message(embed=Error(description=response.content))

    @commands.slash_command(
        name='get-task',
        description='Returns task or task with id or tags'
    )
    async def get_task(
        self,
        inter: disnake.ApplicationCommandInteraction,
        id: int | None = None,
        tags: str | None = None
    ):
        if id:
            response = requests.get(f"{API_URL}/task/?id={id}")
            match response.status_code:
                case 200:
                    task: TypedTask = json.loads(response.content)['task']
                    await self.send_task(inter, task)

                case 404:
                    await inter.response.send_message(embed=Error(description=f'Task has not found with this id: {id}'))

                case _:
                    await inter.response.send_message(embed=Error(description=f'Unknown request error'))
        
        elif tags:
            response = requests.get(f"{API_URL}/tasks/by_tags/?tags={tags}")
            match response.status_code:
                case 200:
                    tasks: list[TypedTask] = json.loads(response.content)['tasks']
                    embed = Info(description=f'Founded {len(tasks)} tasks with tags: {tags}')
                    [embed.add_field(task['title'], task['task'], inline=False) for task in tasks]
                    await inter.response.send_message(embed=embed)

                case 404:
                    await inter.response.send_message(embed=Error(description=f'Tasks have not found with these tags: {tags}'))

                case _:
                    await inter.response.send_message(embed=Error(description=f'Unknown request error'))
        
        else:
            await inter.response.send_message(embed=Error(description=f'YUou must pass at least 1 parameter'))

    async def send_task(self, inter: disnake.AppCommandInteraction, task: TypedTask, /):
        embed = Info()
        embed.set_image(task['image_url'])
        embed.add_field(task['title'], task['topic'], inline=False)
        embed.add_field('Task', task['task'], inline=False)
        await inter.response.send_message(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))
