from datetime import datetime
import json
import datetime
import time
import psutil
import discord
from discord.ext import commands
from json import JSONDecodeError
from discord import TextChannel
from discord import NotFound
import asyncio
from discord.ext.commands import has_permissions
from discord.ext.commands import is_owner
from discord.ext.commands import is_nsfw

bot = commands.Bot(command_prefix='n!')

botcolor = 0x000ffc

bot.remove_command('help')

start_time = time.time()


class users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def isBanned(self, id):
        with open("config/botban.json") as fp:
            data = json.load(fp)
        if str(id) in data:
            return True
        return False

    def version(self):
        with open("config/config.json") as fp:
            data = json.load(fp)
        Token = data['version']
        return str(Token)

    def hasCoins(self, id):
        with open("eco/eco.json") as fp:
            data = json.load(fp)
        if str(id) in data:
            return True
        return False

    def coins(self, user_id):
        if self.hasCoins(user_id):
            with open("eco/eco.json") as fp:
                data = json.load(fp)
            Token = data[user_id]
            return str(Token)
        return str("0")

    @bot.command()
    async def help(self, ctx):
        if self.isBanned(ctx.author.id):
            await ctx.author.send("Na? Wie fühlt sich das, gebannt zu sein?")
            return
        if not ctx.author.bot:
            await ctx.channel.send("`n!help` - `n!about` - `n!setJoinMessage <channel_id/#channel> <nachricht>` - `n!setJoinRole <rollen_id>` - `n!say <nachricht>` - `n!profile`")

    @bot.command()
    async def bal(self, ctx):
        await ctx.channel.send("Du hast **" + str(self.coins(str(ctx.author.id))) + "** Coins")

    @bot.command()
    async def ping(self, ctx):
        await ctx.channel.send("PONG! Mein Ping beträgt gerade **" + str(round(self.bot.latency * 1000)) + "ms**")

    @bot.command()
    async def about(self, ctx):
        if self.isBanned(ctx.author.id):
            await ctx.author.send("Na? Wie fühlt sich das, gebannt zu sein?")
            return
        if ctx.author.bot:
            return
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))

        cpu_per = round(psutil.cpu_percent(), 1)
        mem = psutil.virtual_memory()
        mem_per = round(psutil.virtual_memory().percent, 1)

        description = "Entwickler - **MauricePascal#3009**\n" \
                      "Online seit - **" + text + "**\n" \
                      "Python Version - **3.7.4**\n" \
                      "discord.py Version - **1.3.4**\n" \
                      "Neoben Version - **" + self.version() + "**\n" \
                      "\n" \
                      "Server - **" + str(len(self.bot.guilds)) + "**\n" \
                      "User - **" + str(sum(len(s.members) for s in self.bot.guilds)) + "**\n" \
                      "Ping - **" + str(round(self.bot.latency * 1000))+"ms**\n" \
                      "\n" \
                      "CPU Auslastung - **" + str(cpu_per) + "%**\n" \
                      "RAM Auslastung - **" + str(mem_per) + "%**"
        embed = discord.Embed(title="About", color=botcolor, description=description)
        await ctx.channel.send(embed=embed)

    def joinroleExists(self, guild_id):
        with open("JoinLeave/joinrole.json") as fp:
            data = json.load(fp)
        if str(guild_id) in data:
            return True
        return False

    def joinMessage(self, guild_id):
        with open("JoinLeave/joinmsg.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token["message"])

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

    def leaveMessage(self, guild_id):
        with open("JoinLeave/leavemsg.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token["message"])

    def leavehannel(self, guild_id):
        with open("JoinLeave/leavemsg.json") as fp:
            data = json.load(fp)
        Token = data[str(guild_id)]
        return str(Token["channel_id"])

    def leavemsgExists(self, guild_id):
        with open("JoinLeave/leavemsg.json") as fp:
            data = json.load(fp)
        if str(guild_id) in data:
            return True
        return False

    @bot.command()
    @has_permissions(manage_guild=True)
    async def setJoinRole(self, ctx, args1):
        if self.joinroleExists(ctx.guild.id):
            await ctx.channel.send("JoinRolle wurde bereits gesetzt")
            return
        try:
            with open("JoinLeave/joinrole.json", "r", encoding="utf-8") as fh:
                bans = json.load(fh)
                bans[ctx.guild.id] = args1
                with open("JoinLeave/joinrole.json", "w", encoding="utf-8") as fh:
                    json.dump(bans, fh, indent=4)
                    await ctx.channel.send("JoinRolle gesetzt")
        except JSONDecodeError:
            return

    @bot.command()
    @has_permissions(manage_guild=True)
    async def setJoinMessage(self, ctx, channel:discord.TextChannel, *args:str):
        if self.joinmsgExists(ctx.guild.id):
            await ctx.channel.send("Nachricht und Kanal bereits gesetzt. Bitte melde dich beim Support, wenn du deine Eingaben änder möchtest")
            return
        channel_id = channel.id
        message = ""
        for s in args:
            message += s + " "
        try:
            with open("JoinLeave/joinmsg.json", "r", encoding="utf-8") as fh:
                bans = json.load(fh)
                bans[ctx.guild.id] = {
                    "channel_id": channel_id,
                    "message": message
                }
                with open("JoinLeave/joinmsg.json", "w", encoding="utf-8") as fh:
                    json.dump(bans, fh, indent=4)
                    await ctx.channel.send("joinMessage gesetzt")
        except JSONDecodeError:
            return

    @bot.command()
    @has_permissions(manage_guild=True)
    async def setLeaveMessage(self, ctx, channel:discord.TextChannel, *args:str):
        if self.leavemsgExists(ctx.guild.id):
            await ctx.channel.send("Nachricht und Kanal bereits gesetzt. Bitte melde dich beim Support, wenn du deine Eingaben ändern möchtest")
            return
        channel_id = channel.id
        message = ""
        for s in args:
            message += s + " "
        try:
            with open("JoinLeave/leavemsg.json", "r", encoding="utf-8") as fh:
                bans = json.load(fh)
                bans[ctx.guild.id] = {
                    "channel_id": channel_id,
                    "message": message
                }
                with open("JoinLeave/leavemsg.json", "w", encoding="utf-8") as fh:
                    json.dump(bans, fh, indent=4)
                    await ctx.channel.send("LeaveMessage gesetzt")
        except JSONDecodeError:
            return

    @bot.command()
    async def say(self, ctx, *args:str):
        try:
            message = ""
            for s in args:
                message += s + " "
            embed = discord.Embed(title=ctx.author.name+"#"+ctx.author.discriminator+" sagt:", description=message, color=botcolor)
            await ctx.channel.send(embed=embed)
            await ctx.message.delete()
        except NotFound:
            pass

    async def github(self, user_id:str):
        with open("profile/github.json", "r") as fp:
            data = json.load(fp)
        if user_id not in data:
            return "Nicht gesetzt"
        return data[user_id]

    async def twitter(self, user_id:str):
        with open("profile/twitter.json", "r") as fp:
            data = json.load(fp)
        if user_id not in data:
            return "Nicht gesetzt"
        return data[user_id]

    async def youtube(self, user_id:str):
        with open("profile/youtube.json", "r") as fp:
            data = json.load(fp)
        if user_id not in data:
            return "Nicht gesetzt"
        return data[user_id]

    async def desc(self, user_id:str):
        with open("profile/desc.json", "r") as fp:
            data = json.load(fp)
        if user_id not in data:
            return "Ich bin eine Person, die noch keine Beschreibung hat. \nIch bleibe lieber bei der default Beschreibung"
        return data[user_id]

    @bot.command()
    async def profile(self, ctx, *args):
        length = len(args)
        if int(length) == 0:
            with open("profile/cards.json", "r") as fp:
                data = json.load(fp)
            if str(ctx.author.id) not in data:
                await ctx.channel.send("Du hast noch kein Profil - `n!profile create`")
                return
            youtube = str(await self.youtube(str(ctx.author.id)))
            github = str(await self.github(str(ctx.author.id)))
            twitter = str(await self.twitter(str(ctx.author.id)))
            youtubeRaw = ""
            twitterRaw = ""
            githubRaw = ""

            if not youtube.startswith("https://"):
                youtubeRaw = youtube
            else:
                youtubeRaw = "[Zum Kanal]"+youtube+")"

            if not github.startswith("https://"):
                githubRaw = github
            else:
                githubRaw = "[" + github.replace("https://github.com/", "") + "](" + github + ")"

            if not twitter.startswith("https://"):
                twitterRaw = twitter
            else:
                twitterRaw = "[" + twitter.replace("https://twitter.com/", "") + "](" + twitter + ")"

            description = "**Benutzername**\n" + ctx.author.name+"#"+ctx.author.discriminator + "\n\n" \
                          "**Soziale Medien**\n" \
                          "GitHub - " + githubRaw + "\n" \
                          "Twitter - " + twitterRaw + "\n" \
                          "YouTube - " + youtubeRaw + "\n\n" \
                          "**Beschreibung**\n" + str(await self.desc(str(ctx.author.id)))
            embed = discord.Embed(description=description, color=botcolor)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)
        elif int(length) == 1:
            if args[0] == "create":
                with open("profile/cards.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) in data:
                    await ctx.channel.send("Du hast schon ein Profil. Witzbold")
                else:
                    message = await ctx.channel.send("Profil wird erstellt...")
                    await asyncio.sleep(1)
                    try:
                        with open("profile/cards.json", "r", encoding="utf-8") as fh:
                            bans = json.load(fh)
                            bans[ctx.author.id] = True
                            with open("profile/cards.json", "w", encoding="utf-8") as fh:
                                json.dump(bans, fh, indent=4)
                                await message.edit(content="Profil wurde erstellt")
                    except JSONDecodeError:
                        return
        elif int(length) >= 2:
            if args[0] == "desc":
                with open("profile/cards.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) not in data:
                    await ctx.channel.send("Du hast noch kein Profil - `n!profile create`")
                    return
                with open("profile/desc.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) in data:
                    with open("profile/desc.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[str(ctx.author.id)] = True
                        with open("profile/desc.json", "w", encoding="utf-8") as fh:
                            del bans[str(ctx.author.id)]
                            json.dump(bans, fh, indent=4)
                desc = ""
                for s in args:
                    desc += s + " "
                try:
                    with open("profile/desc.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[ctx.author.id] = desc.replace("desc ", "")
                        with open("profile/desc.json", "w", encoding="utf-8") as fh:
                            json.dump(bans, fh, indent=4)
                            await ctx.channel.send("Beschreibung wurde erfolgreich gesetzt")
                except JSONDecodeError:
                    return
            elif args[0] == "github":
                with open("profile/cards.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) not in data:
                    await ctx.channel.send("Du hast noch kein Profil - `n!profile create`")
                    return
                if args[1] == "remove":
                    with open("profile/github.json", "r") as fp:
                        data = json.load(fp)
                    if str(ctx.author.id) in data:
                        with open("profile/github.json", "r", encoding="utf-8") as fh:
                            bans = json.load(fh)
                            bans[str(ctx.author.id)] = True
                            with open("profile/github.json", "w", encoding="utf-8") as fh:
                                del bans[str(ctx.author.id)]
                                json.dump(bans, fh, indent=4)
                                await ctx.send("Dein GitHub Account wurde entfernt")
                                return
                    else:
                        await ctx.send("Du bist ja mal einer. Du hast garkein Twitter Account verlinkt")
                        return
                if not int(length) == 2:
                    await ctx.send("Ich bezweifel, dass das dein GitHub Name ist")
                    return
                if args[1].startswith("https://"):
                    await ctx.send("Du sollst mir nur deinen Namen verraten")
                    return
                with open("profile/github.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) in data:
                    with open("profile/github.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[str(ctx.author.id)] = True
                        with open("profile/github.json", "w", encoding="utf-8") as fh:
                            del bans[str(ctx.author.id)]
                            json.dump(bans, fh, indent=4)
                try:
                    with open("profile/github.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[ctx.author.id] = "https://github.com/"+args[1]
                        with open("profile/github.json", "w", encoding="utf-8") as fh:
                            json.dump(bans, fh, indent=4)
                            await ctx.channel.send("Github wurde erfolgreich gesetzt")
                except JSONDecodeError:
                    return
            elif args[0] == "twitter":
                with open("profile/cards.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) not in data:
                    await ctx.channel.send("Du hast noch kein Profil - `n!profile create`")
                    return
                if args[1] == "remove":
                    with open("profile/twitter.json", "r") as fp:
                        data = json.load(fp)
                    if str(ctx.author.id) in data:
                        with open("profile/twitter.json", "r", encoding="utf-8") as fh:
                            bans = json.load(fh)
                            bans[str(ctx.author.id)] = True
                            with open("profile/twitter.json", "w", encoding="utf-8") as fh:
                                del bans[str(ctx.author.id)]
                                json.dump(bans, fh, indent=4)
                                await ctx.send("Dein Twitter Account wurde entfernt")
                                return
                    else:
                        await ctx.send("Du bist ja mal einer. Du hast garkein Twitter Account verlinkt")
                        return
                if not int(length) == 2:
                    await ctx.send("Ich bezweifel, dass das dein Twitter Name ist")
                    return
                if args[1].startswith("https://"):
                    await ctx.send("Du sollst mir nur deinen Namen verraten")
                    return
                with open("profile/twitter.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) in data:
                    with open("profile/twitter.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[str(ctx.author.id)] = True
                        with open("profile/twitter.json", "w", encoding="utf-8") as fh:
                            del bans[str(ctx.author.id)]
                            json.dump(bans, fh, indent=4)
                try:
                    with open("profile/twitter.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[ctx.author.id] = "https://twitter.com/"+args[1]
                        with open("profile/twitter.json", "w", encoding="utf-8") as fh:
                            json.dump(bans, fh, indent=4)
                            await ctx.channel.send("Twitter wurde erfolgreich gesetzt")
                except JSONDecodeError:
                    return
            elif args[0] == "yt":
                with open("profile/cards.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) not in data:
                    await ctx.channel.send("Du hast noch kein Profil - `n!profile create`")
                    return
                if args[1] == "remove":
                    with open("profile/youtube.json", "r") as fp:
                        data = json.load(fp)
                    if str(ctx.author.id) in data:
                        with open("profile/youtube.json", "r", encoding="utf-8") as fh:
                            bans = json.load(fh)
                            bans[str(ctx.author.id)] = True
                            with open("profile/youtube.json", "w", encoding="utf-8") as fh:
                                del bans[str(ctx.author.id)]
                                json.dump(bans, fh, indent=4)
                                await ctx.send("Dein YouTube Account wurde entfernt")
                                return
                    else:
                        await ctx.send("Du bist ja mal einer. Du hast garkein YouTube Account verlinkt")
                        return
                if not args[1].startswith("https://youtube.com/"):
                    await ctx.send("Du sollst mir einen Link geben")
                    return
                with open("profile/youtube.json", "r") as fp:
                    data = json.load(fp)
                if str(ctx.author.id) in data:
                    with open("profile/youtube.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[str(ctx.author.id)] = True
                        with open("profile/youtube.json", "w", encoding="utf-8") as fh:
                            del bans[str(ctx.author.id)]
                            json.dump(bans, fh, indent=4)
                try:
                    with open("profile/youtube.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[ctx.author.id] = args[1]
                        with open("profile/youtube.json", "w", encoding="utf-8") as fh:
                            json.dump(bans, fh, indent=4)
                            await ctx.channel.send("YouTube wurde erfolgreich gesetzt")
                except JSONDecodeError:
                    return


def setup(bot):
    bot.add_cog(users(bot))
