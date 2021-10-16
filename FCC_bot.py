import discord
import os
from discord.ext import commands

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

# These commands handle loading and unloading things from the cogs file.


async def post_log(ctx, message: str):
    server = ctx.guild
    log_channel = discord.utils.get(
        server.text_channels, name="bot-logs")
    await log_channel.send(message)


@commands.has_role('Admin')
@client.command(hidden=True)
async def load(ctx, extension):
    try:
        print(f'{extension} were loaded manually')
        client.load_extension(f'FCC_cogs.{extension}')
        await post_log(ctx, f"✅ LOAD: USER: {ctx.message.author} LOADS: {extension}")
    except Exception as error:
        await post_log(ctx, f"🚨 LOAD: USER: {ctx.message.author} LOADS: {extension}")
        await post_log(ctx, f"```python {error}```")
        raise(error)


@commands.has_role('Admin')
@client.command(hidden=True)
async def unload(ctx, extension):
    try:
        client.unload_extension(f'FCC_cogs.{extension}')
        await post_log(ctx, f"✅ UNLOAD: USER: {ctx.message.author} UNLOADS: {extension}")
        print(f'{extension} were unloaded manually')
    except Exception as error:
        await post_log(ctx, f"🚨 UNLOAD: USER: {ctx.message.author} UNLOADS: {extension}")
        await post_log(ctx, f"```python {error}```")
        raise(error)


@commands.has_role("Admin")
@client.command(hidden=True)
async def reload(ctx, ext):
    try:
        client.unload_extension(f'FCC_cogs.{ext}')
        client.load_extension(f'FCC_cogs.{ext}')
        print(f'Reloading cog {ext}')
        await post_log(ctx, f"✅ RELOAD: USER: {ctx.message.author} RELOADS: {ext}")
    except Exception as error:
        await post_log(ctx, f"🚨 RELOAD: USER: {ctx.message.author} RELOADS: {ext}")
        await post_log(ctx, f"```python {error}```")
        raise(error)


@commands.has_role("Admin")
@client.command(hidden=True, aliases=['rfr'])
async def make_rfr_post(ctx):
    server = ctx.guild
    RFR_channel = discord.utils.get(
        server.text_channels, name="react-for-roles")

    await post_log(ctx, f"🔥 TRIGGER: USER: {ctx.message.author} Request react-for-roles post")

    await RFR_channel.send("Use the reactions to assign yourself roles!")
    await RFR_channel.send("🇰🇷 is Seoul-based\n🏙️ is Ulsan-based\n🌉 is Busan-based\n🛫 is Overseas-based")
    await RFR_channel.send("You can select multiple locations. Your user colour reflects the highest role on this list.\nUsers with no location-based roles will be green!\nIf your roles get messed up, message server owner Tobio.")


for filename in os.listdir('./FCC_cogs'):
    if filename.endswith('.py'):

        # The -3 cuts off the .py to conform with the correct syntax
        client.load_extension(f'FCC_cogs.{filename[:-3]}')
        print(f'Loaded cogs from {filename}')

client.run(os.environ.get('BOT_KEY'))
