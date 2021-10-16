import discord
import os
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

# These commands handle loading and unloading things from the cogs file.


@commands.has_role('Admin')
@client.command(hidden=True)
async def load(_, extension):
    print(f'{extension} were loaded manually')
    client.load_extension(f'FCC_cogs.{extension}')


@commands.has_role('Admin')
@client.command(hidden=True)
async def unload(_, extension):
    print(f'{extension} were unloaded manually')
    client.unload_extension(f'FCC_cogs.{extension}')


@commands.has_role("Admin")
@client.command(hidden=True)
async def reload(_, ext):
    print(f'Reloading cog {ext}')
    client.unload_extension(f'FCC_cogs.{ext}')
    client.load_extension(f'FCC_cogs.{ext}')


@commands.has_role("Admin")
@client.command(hidden=True, aliases=['rfr'])
async def make_rfr_post(ctx):
    server = ctx.guild
    RFR_channel = discord.utils.get(
        server.text_channels, name="react-for-roles")

    await RFR_channel.send("Use the reactions to assign yourself roles!")
    await RFR_channel.send("🇰🇷 is Seoul-based\n🏙️ is Ulsan-based\n🌉 is Busan-based\n🛫 is Overseas-based")
    await RFR_channel.send("You can select multiple locations. Your user colour reflects the highest role on this list.\nUsers with no location-based roles will be green!\nIf your roles get messed up, message server owner Tobio.")


for filename in os.listdir('./FCC_cogs'):
    if filename.endswith('.py'):

        # The -3 cuts off the .py to conform with the correct syntax
        client.load_extension(f'FCC_cogs.{filename[:-3]}')
        print(f'Loaded cogs from {filename}')

client.run(os.environ.get('BOT_KEY'))
