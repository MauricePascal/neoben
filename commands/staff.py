from datetime import datetime
import json

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='n!')

botcolor = 0x000ffc

bot.remove_command('help')


class staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self):
        return

def setup(bot):
    bot.add_cog(staff(bot))