from datetime import datetime

import discord
import json
import ast
from discord.ext import commands
from discord import NotFound
from discord import HTTPException
from json import JSONDecodeError
import asyncio

bot = commands.Bot(command_prefix='n!')

botcolor = 0x000ffc

bot.remove_command('help')


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def isBanned(self, id):
        with open("config/botban.json") as fp:
            data = json.load(fp)
        if str(id) in data:
            return True
        return False

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

    @commands.command()
    async def coinadmin(self, ctx, *args:str):
        if not ctx.author.id == 622784776234991626:
            msg = await ctx.channel.send("Du bist aber neugierig")
            await asyncio.sleep(3)
            await msg.delete()
            return
        length = len(args)
        if int(length) == 3:
            if args[0] == "set":
                user_id = args[1]
                amt = args[2]
                if self.hasCoins(user_id):
                    with open("eco/eco.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[user_id] = True
                        with open("eco/eco.json", "w", encoding="utf-8") as fh:
                            del bans[user_id]
                            json.dump(bans, fh, indent=4)
                    try:
                        with open("eco/eco.json", "r", encoding="utf-8") as fh:
                            bans = json.load(fh)
                            bans[user_id] = amt
                            with open("eco/eco.json", "w", encoding="utf-8") as fh:
                                json.dump(bans, fh, indent=4)
                                await ctx.channel.send("Erfolgreich auf **" + amt + "** gesetzt")
                    except JSONDecodeError:
                        return
                else:
                    try:
                        with open("eco/eco.json", "r", encoding="utf-8") as fh:
                            bans = json.load(fh)
                            bans[user_id] = amt
                            with open("eco/eco.json", "w", encoding="utf-8") as fh:
                                json.dump(bans, fh, indent=4)
                                await ctx.channel.send("Erfolgreich auf **" + amt + "** gesetzt")
                    except JSONDecodeError:
                        return
            elif args[0] == "remove":
                user_id = args[1]
                amt = args[2]
                if self.hasCoins(user_id):
                    newAmt = str(int(self.coins(user_id)) - int(amt))
                    with open("eco/eco.json", "r", encoding="utf-8") as fh:
                        bans = json.load(fh)
                        bans[user_id] = newAmt
                        with open("eco/eco.json", "w", encoding="utf-8") as fh:
                            del bans[user_id]
                            json.dump(bans, fh, indent=4)
                        try:
                            if int(newAmt) < int(0):
                                await ctx.channel.send("Du als Admin solltest aber wissen, dass man nicht ins Minus gehen kann")
                                return
                            with open("eco/eco.json", "r", encoding="utf-8") as fh:
                                print(newAmt)
                                bans = json.load(fh)
                                bans[user_id] = str(newAmt)
                                with open("eco/eco.json", "w", encoding="utf-8") as file:
                                    json.dump(bans, file, indent=4)
                                    await ctx.channel.send("Erfolgreich auf **" + newAmt + "** gesetzt")
                        except JSONDecodeError:
                            return
                else:
                    await ctx.channel.send("Du als Admin solltest aber wissen, dass man nicht ins Minus gehen kann")

    # @commands.command()
    # async def inviteInfo(self, ctx, *, args):
    #     if not ctx.author.bot:
    #         if ctx.author.id == 622784776234991626:
    #             try:
    #                 invite = await self.bot.fetch_invite(args)
    #                 await ctx.channel.send("KK")
    #                 print(str(invite.uses))
    #             except NotFound:
    #                 await ctx.channel.send("Invite not found")
    #             except HTTPException:
    #                 await ctx.channel.send("Error")

    @commands.command()
    async def statsetup(self, ctx):
        if ctx.author.id == 622784776234991626:
            guilds = list(s for s in self.bot.guilds)
            member = sum(len(s.members) for s in self.bot.guilds)
            channel1 = self.bot.get_channel(732376809672540230)
            channel4 = self.bot.get_channel(732376787920879706)
            await channel1.edit(name="Total Users: {}".format(member))
            await channel4.edit(name="Server: {}".format(str(len(guilds))))

    @commands.command()
    async def shutdown(self, ctx):
        if not ctx.author.bot:
            if not ctx.author.id == 622784776234991626:
                msg = await ctx.channel.send("Du bist aber neugierig")
                await asyncio.sleep(3)
                await msg.delete()
                return
            if ctx.author.id == 622784776234991626:
                await self.bot.change_presence(status=discord.Status.offline)
                await ctx.channel.send("Good night")
                await self.bot.close()

    @commands.command()
    async def bban(self, ctx, args1):
        if not ctx.author.id == 622784776234991626:
            msg = await ctx.channel.send("Du bist aber neugierig")
            await asyncio.sleep(3)
            await msg.delete()
            return
        try:
            with open("config/botban.json", "r", encoding="utf-8") as fh:
                bans = json.load(fh)
                bans[args1] = True
                with open("config/botban.json", "w", encoding="utf-8") as fh:
                    json.dump(bans, fh, indent=4)
                    await ctx.channel.send("Done")
                    channel = self.bot.get_channel(732402393764986891)
                    await channel.send("ID " + args1 + " wurde vom Bot entbannt von <@" + ctx.author.id+">")
        except JSONDecodeError:
            return

    @commands.command()
    async def bunban(self, ctx, args1):
        if not ctx.author.id == 622784776234991626:
            msg = await ctx.channel.send("Du bist aber neugierig")
            await asyncio.sleep(3)
            await msg.delete()
            return
        try:
            with open("config/botban.json", "r", encoding="utf-8") as fh:
                bans = json.load(fh)
                bans[args1] = True
                with open("config/botban.json", "w", encoding="utf-8") as fh:
                    del bans[args1]
                    json.dump(bans, fh, indent=4)
                    await ctx.channel.send("Done")
                    channel = self.bot.get_channel(732402393764986891)
                    await channel.send("ID " + args1 + " wurde vom Bot gebannt von <@" + ctx.author.id+">")
        except JSONDecodeError:
            return

    @commands.command()
    async def chatban(self, ctx, args1):
        if not ctx.author.id == 622784776234991626:
            msg = await ctx.channel.send("Du bist aber neugierig")
            await asyncio.sleep(3)
            await msg.delete()
            return
        try:
            with open("config/chatban.json", "r", encoding="utf-8") as fh:
                bans = json.load(fh)
                bans[args1] = True
                with open("config/chatban.json", "w", encoding="utf-8") as fh:
                    json.dump(bans, fh, indent=4)
                    await ctx.channel.send("Done")
                    channel = self.bot.get_channel(732402393764986891)
                    await channel.send("ID " + args1 + " wurde von dem Globalchat entbannt von <@" + ctx.author.id+">")
        except JSONDecodeError:
            return

    @commands.command()
    async def chatunban(self, ctx, args1):
        if not ctx.author.id == 622784776234991626:
            msg = await ctx.channel.send("Du bist aber neugierig")
            await asyncio.sleep(3)
            await msg.delete()
            return
        try:
            with open("config/chatban.json", "r", encoding="utf-8") as fh:
                bans = json.load(fh)
                bans[args1] = True
                with open("config/chatban.json", "w", encoding="utf-8") as fh:
                    del bans[args1]
                    json.dump(bans, fh, indent=4)
                    await ctx.channel.send("Done")
                    channel = self.bot.get_channel(732402393764986891)
                    await channel.send("ID " + args1 + " wurde aus dem Globalchat gebannt von <@" + ctx.author.id+">")
        except JSONDecodeError:
            return

    @commands.command()
    async def eval(self, ctx, *, cmd):
        if not ctx.author.id == 622784776234991626:
            msg = await ctx.channel.send("Du bist aber neugierig")
            await asyncio.sleep(3)
            await msg.delete()
            return
        """Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
          - `bot`: the bot instance
          - `discord`: the discord module
          - `commands`: the discord.ext.commands module
          - `ctx`: the invokation context
          - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating
        >eval ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.author.send(result)


def setup(bot):
    bot.add_cog(dev(bot))
