import disnake
import services.api as api
from disnake.ext import commands

class MemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot, /):
        super().__init__()
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(MemberCog(bot))
