import discord
from discord.ext import commands


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()  # This is equal to @client.event, but for cogs.
    async def on_ready(self):
        print('FCC Bot is activated...')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'User {member} has joined.')
        server = member.guild
        general_channel = discord.utils.get(
            server.text_channels, name="off-topic")
        newcomer_role = discord.utils.get(server.roles, name="No-location")
        await member.add_roles(newcomer_role)
        await general_channel.send(f"Welcome, @{member}! Feel free to visit the react-for-roles room and let us know where you're based!")

    # Commands

    # This allows you to do commands.
    @commands.command(brief='Find out your latency!')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms.')

    @commands.has_role('Admin')
    @commands.command(aliases=['erase'], brief='Erases one message by default.', hidden=True)
    async def clear(self, ctx, amount=1, pw=None):
        if amount > 5:

            if pw == 'begone':
                print('Correct password!')

            else:
                print(f'Password {pw} was wrong, capped at 5')
                amount = 5

        # The +1 is because to erase the messages, the bot replies.
        await ctx.channel.purge(limit=amount+1)

    @commands.has_role('Admin')
    @commands.command(brief='Change the bot status', hidden=True)
    async def status(self, ctx, status):
        statuses = {
            'idle': discord.Status.idle,
            'online': discord.Status.online,
            'offline': discord.Status.offline,
            'dnd': discord.Status.do_not_disturb,
            'invisible': discord.Status.invisible
        }
        print(f'Changed status to {status}')
        if status == 'help':
            await ctx.send('Status can be: online, idle, dnd, invisible and offline.')

        try:
            # This line is about statuses
            await self.client.change_presence(status=statuses[status])
        except:
            await ctx.send(f"Nope, I'm not being {status}. Try online, idle, dnd, invisible or offline")


def setup(client):
    client.add_cog(Basic(client))
