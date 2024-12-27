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

    @commands.slash_command(name='random-task')
    async def get_random_task(self, inter: disnake.ApplicationCommandInteraction):
        response = requests.get(f"{API_URL}/tasks/ids/")
        if response.ok:
            tasks_ids: list[int] = json.loads(response.content)['ids']

            if tasks_ids:
                response = requests.get(f"{API_URL}/task/", headers={
                    'body':json.dumps({
                        'id':random.choice(tasks_ids)
                    })
                })
                if response.ok:
                    task: TypedTask = json.loads(response.content)['task']
                    embed = Info()
                    embed.add_field(task['title'], task['text'])
                    await inter.response.send_message(embed=embed)
                
                else:
                    await inter.response.send_message(embed=Error(description=f'Request error: {response.content}'))
            
            else:
                await inter.response.send_message(embed=Error(description='No tasks available'))
    
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
            response = requests.get(f"{API_URL}/task/", headers={
                'body':json.dumps({
                    'id':id
                })
            })
            if response.ok:
                task: TypedTask = json.loads(response.content)['task']
                embed = Info()
                embed.add_field(task['title'], task['text'])
                await inter.response.send_message(embed=embed)
            
            elif response.status_code == 404:
                await inter.response.send_message(embed=Error(description=f'Task has not found with this id: {id}'))
            
            else:
                await inter.response.send_message(embed=Error(description=f'Unknown request error'))
        
        elif tags:
            response = requests.get(f"{API_URL}/tasks/by_tags", headers={
                'body':json.dumps({
                    'tags':tags.replace(' ', '').split(',') # delete spaces and split by ,
                })
            })
            if response.ok:
                tasks: list[TypedTask] = json.loads(response.content)['tasks']
                embed = Info(description=f'Founded {len(tasks)} tasks with tags: {tags}')
                [embed.add_field(task['title'], task['text'], inline=False) for task in tasks]
                await inter.response.send_message(embed=embed)
            
            elif response.status_code == 404:
                await inter.response.send_message(embed=Error(description=f'Tasks have not found with these tags: {tags}'))
            
            else:
                await inter.response.send_message(embed=Error(description=f'Unknown request error'))
        
        else:
            await inter.response.send_message(embed=Error(description=f'YUou must pass at least 1 parameter'))


def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))
