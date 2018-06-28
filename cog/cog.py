import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        """This does stuff!"""

        if not after.nick.printable():
                await self.bot.change_nickname(after, None)
                
        await self.bot.say("I can do stuff!")

def setup(bot):
    bot.add_cog(Mycog(bot))
