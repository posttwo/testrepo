from datetime import datetime
import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import pagify, box, warning, error, info, bold

PATH = 'data/blocknamechange/'
JSON = PATH + 'settings.json'

class Mycog:

    def __init__(self, bot):
        self.bot = bot
        self.json = compat_load(JSON)

        try:
            self.analytics = CogAnalytics(self)
        except Exception as error:
            self.bot.logger.exception(error)
            self.analytics = None
     
    def __unload(self):
        self.save()
        
    def save(self):
        dataIO.save_json(JSON, self.json)
    
    
    @commands.group(pass_context=True, invoke_without_command=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def punish(self, ctx, member: discord.Member):
        if ctx.invoked_subcommand is None:
            if member:
                msg = ''
                server = ctx.message.server
                mod = self.bot.get_cog('Mod')
                if server.id not in self.json:
                    self.json[server.id] = {}
                current = self.json[server.id].get(member.id, {})
                
                if member.id in self.json[server.id]:
                    msg =+ '{0} is already unable to change nickname'
                else    
                    self.json[server.id][member.id] = { 
                       'start' : current.get('start') or now,
                       'by': current.get('by') or ctx.message.author.id
                    }
                    msg =+ '{0} is now unable to change nickname'
                
                msg = msg.format(member)
                
                await self.bot.say(msg)
    
            else:
                await self.bot.send_cmd_help(ctx)
                
    async def on_member_update(self, before, after):
        """This does stuff!"""

        if after.nick.contains('឵឵ ឵឵'):
                await self.bot.change_nickname(after, None)
                
        await self.bot.say("I can do stuff!")
        
    

def setup(bot):
    bot.add_cog(Mycog(bot))

    
    
def compat_load(path):
    data = dataIO.load_json(path)
    for server, punishments in data.items():
        for user, pdata in punishments.items():
            if not user.isdigit():
                continue

            # read Kownlin json
            by = pdata.pop('givenby', None)
            by = by if by else pdata.pop('by', None)
            pdata['by'] = by
            pdata['reason'] = pdata.pop('reason', None)

    return data
