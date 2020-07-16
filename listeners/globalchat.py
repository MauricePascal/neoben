from datetime import datetime
import asyncio
import discord
from discord.ext import commands
from discord import NotFound
import json

bot = commands.Bot(command_prefix='n!')

botcolor = 0x000ffc

bot.remove_command('help')


class globalchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def isBanned(self, id):
        with open("config/botban.json") as fp:
            data = json.load(fp)
        if str(id) in data:
            return True
        return False

    def isChatBanned(self, id):
        with open("config/chatban.json") as fp:
            data = json.load(fp)
        if str(id) in data:
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            message.channel.name
        except AttributeError:
            return
        if not message.channel.name == 'neo-global':
            return
        if self.isChatBanned(message.author.id):
            await message.author.send("Upsi, du wurdest wohl aus dem Chat gebannt")
            try:
                await message.delete()
            except NotFound:
                pass
            return
        if self.isBanned(message.author.id):
            await message.author.send("Na? Wie fühlt sich das, gebannt zu sein?")
            try:
                await message.delete()
            except NotFound:
                pass
            return
        if not message.channel.name == 'neo-global':
            return
        if message.channel.id == 732903779996926032:
            return
        for g in self.bot.guilds:
            for ch in g.channels:
                if ch.name == "neo-global":
                    if message.author.bot:
                        if message.author.id == self.bot.user.id:
                            return
                        await message.delete()
                        return
                    if not ch.id == 732903779996926032:
                        if message.author.id == 622784776234991626:
                            content = message.content
                            embed = discord.Embed(title=None, url=None, description=content, color=0x00fffc)
                            embed.set_footer(text="ID - " + str(message.author.id) + " | Server - " + message.guild.name)
                            embed.set_author(name=message.author.name+"#"+message.author.discriminator, icon_url=message.author.avatar_url)
                            await ch.send(embed=embed)
                            try:
                                await message.delete()
                            except NotFound:
                                pass
                        else:
                            content = message.content
                            embed = discord.Embed(title=None, url=None, description=content, color=botcolor)
                            embed.set_footer(text="ID - " + str(message.author.id) + " | Server - " + message.guild.name)
                            embed.set_author(name=message.author.name+"#"+message.author.discriminator, icon_url=message.author.avatar_url)
                            await ch.send(embed=embed)
                            try:
                                await message.delete()
                            except NotFound:
                                pass


def setup(bot):
    bot.add_cog(globalchat(bot))
