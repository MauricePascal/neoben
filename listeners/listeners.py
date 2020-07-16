from datetime import datetime
import asyncio
import discord
import json
from discord.ext import commands
from discord import Forbidden
from discord import NotFound

bot = commands.Bot(command_prefix='n!')

botcolor = 0x000ffc

bot.remove_command('help')


class listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def joinroleExists(self, guild_id):
        with open("JoinLeave/joinrole.json") as fp:
            data = json.load(fp)
        if str(guild_id) in data:
            return True
        return False

    def version(self):
        with open("config/config.json") as fp:
            data = json.load(fp)
        Token = data['version']
        return str(Token)

    def joinrole(self, guild_id):
        with open("JoinLeave/joinrole.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token)

    def joinMessage(self, guild_id):
        with open("JoinLeave/joinmsg.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token["message"])

    def leaveMessage(self, guild_id):
        with open("JoinLeave/leavemsg.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token["message"])

    def leaveChannel(self, guild_id):
        with open("JoinLeave/leavemsg.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token["channel_id"])

    def joinChannel(self, guild_id):
        with open("JoinLeave/joinmsg.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token["channel_id"])

    def joinmsgExists(self, guild_id):
        with open("JoinLeave/joinmsg.json") as fp:
            data = json.load(fp)
        if str(guild_id) in data:
            return True
        return False

    def leavemsgExists(self, guild_id):
        with open("JoinLeave/leavemsg.json") as fp:
            data = json.load(fp)
        if str(guild_id) in data:
            return True
        return False

    @commands.Cog.listener()
    async def on_disconnect(self):
        print("Verbindung zu Discord verloren")

    @commands.Cog.listener()
    async def on_reconnect(self):
        print("Verbindung zu Discord wurde neu aufgebaut")

    @commands.Cog.listener()
    async def on_connect(self):
        print("Erfolgreich zu Discord verbunden")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Erfolgreich Eingeloggt als " + self.bot.user.name + "#" + self.bot.user.discriminator)
        bot.loop.create_task(self.status_task())

    async def status_task(self):
        while True:
            guilds = list(s for s in self.bot.guilds)
            await self.bot.change_presence(activity=discord.Game('n!help'), status=discord.Status.online)
            await asyncio.sleep(30)
            await self.bot.change_presence(activity=discord.Game('auf ' + str(len(guilds)) + " Servern"), status=discord.Status.online)
            await asyncio.sleep(30)
            await self.bot.change_presence(activity=discord.Game('In der Version ' + self.version()), status=discord.Status.online)
            await asyncio.sleep(30)

    #########################################################################################################################
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guilds = list(s for s in self.bot.guilds)
        member = sum(len(s.members) for s in self.bot.guilds)
        channel1 = self.bot.get_channel(732376809672540230)
        channel4 = self.bot.get_channel(732376787920879706)
        await channel1.edit(name="Total Users: {}".format(member))
        await channel4.edit(name="Server: {}".format(str(len(guilds))))

    #########################################################################################################################
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guilds = list(s for s in self.bot.guilds)
        member = sum(len(s.members) for s in self.bot.guilds)
        channel1 = self.bot.get_channel(732376809672540230)
        channel4 = self.bot.get_channel(732376787920879706)
        await channel1.edit(name="Total Users: {}".format(member))
        await channel4.edit(name="Server: {}".format(str(len(guilds))))

    #########################################################################################################################
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 732401762161655829:
            await message.add_reaction("👍")
            await message.add_reaction("👎")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # JoinRole
        if self.joinroleExists(member.guild.id):
            role_id = self.joinrole(member.guild.id)
            try:
                role = member.guild.get_role(role_id=int(role_id))
                try:
                    await member.add_roles(role, reason="JoinRole by Neoben", atomic=True)
                except Forbidden:
                    await member.guild.owner.send(
                        "Ich konnte dem User " + member.name + "#" + member.discriminator + "keine Rolle zuweisen")
            except NotFound:
                await member.guild.owner.send("Ich konnte die angegebene Rollen ID (" + role_id + ") nicht finden")
        # JoinMessage
        if self.joinmsgExists(member.guild.id):
            channel = self.bot.get_channel(int(self.joinChannel(member.guild.id)))
            message = self.joinMessage(member.guild.id)
            await channel.send(message.replace("{user.mention}", "<@"+str(member.id)+">").replace("{user.name}", member.name).replace("{server.count}", str(len(member.guild.members))).replace("{user.hashtag}", member.discriminator).replace("{user.tag}", member.name+"#"+member.discriminator).replace("{server.name}", member.guild.name))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.leavemsgExists(member.guild.id):
            channel = self.bot.get_channel(int(self.leaveChannel(member.guild.id)))
            message = self.leaveMessage(member.guild.id)
            await channel.send(message.replace("{user.mention}", "<@"+str(member.id)+">").replace("{user.name}", member.name).replace("{server.count}", str(len(member.guild.members))).replace("{user.hashtag}", member.discriminator).replace("{user.tag}", member.name+"#"+member.discriminator).replace("{server.name}", member.guild.name))


def setup(bot):
    bot.add_cog(listeners(bot))