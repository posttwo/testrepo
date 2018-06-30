from datetime import datetime
import discord
from discord.ext import commands
from .utils.dataIO import dataIO
from .utils import checks
from .utils.chat_formatting import pagify, box, warning, error, info, bold
import os
import time

PATH = 'data/blocknamechange/'
JSON = PATH + 'settings.json'

class Mycog:

    def __init__(self, bot):
        self.bot = bot
        self.json = compat_load(JSON)
     
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
                    msg += '{0} is already unable to change nickname'
                else:
                    now = time.time()
                    self.json[server.id][member.id] = { 
                       'start' : current.get('start') or now,
                       'by': current.get('by') or ctx.message.author.id
                    }
                    msg += '{0} is now unable to change nickname'
                
                msg = msg.format(member)
                
                await self.bot.say(msg)
                self.save()
    
            else:
                await self.bot.send_cmd_help(ctx)
    
    
    @commands.group(pass_context=True, no_pm=True, name='remove')
    @checks.mod_or_permissions(manage_messages=True)
    async def punish_remove(self, ctx, member: discord.Member):
        self.json[ctx.message.server.id].pop(member.id, None)
        self.save()
    
    @punish.command(pass_context=True, no_pm=True, name='list')
    async def punish_list(self, ctx):
        server = ctx.message.server
        
        for member_id, data in self.json.get(server.id, {}).items():
            if not member_id.isdigit():
                continue
            msg = ('{0} added to list by {1} on {2}')
            msg = msg.format(getmname(member_id, server), getmname(data['by'], server), data['start'])
            await self.bot.say(msg)
        
        
    """async def on_member_update(self, before, after):

        if after.nick.contains('឵឵ ឵឵'):
                await self.bot.change_nickname(after, None)
                
        await self.bot.say("I can do stuff!")"""
        
    

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Mycog(bot))

def check_file():
    if not dataIO.is_valid_json(JSON):
        print('Creating empty %s' % JSON)
        dataIO.save_json(JSON, {})
    
def check_folder():
    if not os.path.exists(PATH):
        print('Creating folder: data/blocknamechange')
        os.makedirs(PATH)

def getmname(mid, server):
    member = discord.utils.get(server.members, id=mid)

    if member:
        return str(member)
    else:
        return '(absent user #%s)' % mid
        
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

    return data
