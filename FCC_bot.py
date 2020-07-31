import discord, os
from discord.ext import commands

client = commands.Bot(command_prefix='!')

# These commands handle loading and unloading things from the cogs file.
@commands.has_role('Admin')
@client.command(hidden=True)
async def load(ctx, extension):
    print(f'{extension} were loaded manually')
    client.load_extension(f'FCC_cogs.{extension}')

@commands.has_role('Admin')
@client.command(hidden=True)
async def unload(ctx, extension):
    print(f'{extension} were unloaded manually')
    client.unload_extension(f'FCC_cogs.{extension}')


for filename in os.listdir('./FCC_cogs'):
    if filename.endswith('.py'):
        
        client.load_extension(f'FCC_cogs.{filename[:-3]}') # The -3 cuts off the .py to conform with the correct syntax
        print(f'Loaded cogs from {filename}')

client.run(os.environ.get('BOT_KEY'))

