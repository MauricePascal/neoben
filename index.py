import json

from discord.ext import commands
from discord.ext.commands import MissingPermissions

########################################################################

client = commands.Bot(command_prefix=commands.when_mentioned_or("n!"))

client.remove_command('help')

extensions = ['commands.dev', 'listeners.listeners', 'listeners.globalchat', 'commands.staff', 'commands.premium', 'commands.users']


def token():
    with open("config/config.json") as fp:
        data = json.load(fp)
    Token = data['token']
    return str(Token)


TOKEN = str(token())

if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} konnte nicht geladen werden. [{}]'.format(extension, error))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, MissingPermissions):
        await ctx.channel.send("Dazu hast du keine Rechte!")


# Invite: https://discord.com/api/oauth2/authorize?client_id=732299049818128414&permissions=8&scope=bot
client.run(TOKEN)
