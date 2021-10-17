import discord
from discord.ext import commands


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.server = None
        self.log_channel = None

    async def post_log(self, message: str):
        if (self.server and self.log_channel):
            await self.log_channel.send(message)

    # Events
    @commands.Cog.listener()  # This is equal to @client.event, but for cogs.
    async def on_ready(self):
        print('FCC Bot is activated...')
        self.server = discord.utils.get(self.client.guilds)
        self.log_channel = discord.utils.get(
            self.server.text_channels, name="bot-logs")
        print("INIT: Logger operational")
        await self.post_log("💡 INIT: Logger operational")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'User {member} has joined.')
        server = member.guild
        general_channel = discord.utils.get(
            server.text_channels, name="off-topic")
        newcomer_role = discord.utils.get(server.roles, name="No-location")
        await member.add_roles(newcomer_role)
        await general_channel.send(f"Welcome, @{member}! Feel free to visit the react-for-roles room and let us know where you're based!")
        await self.post_log(f"🆕 NEW MEMBER: user {member} joined")

    # Commands

    # This allows you to do commands.

    @commands.command(brief='Find out your latency!')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms.')
        await self.post_log(f"🏓 PING: by member {ctx.message.author}")

    @commands.has_role('Admin')
    @commands.command()
    async def forcelog(self, ctx, *, message):
        if type(message) is str:
            await self.post_log(f"📝 FORCELOG: USER: `{ctx.message.author}` FORCELOGS:\n```{message}```")
        else:
            await self.post_log(f"📝 FORCELOG: USER: `{ctx.message.author}` FORCELOGS:\n```" + " ".join(message) + "```")

    @commands.has_role('Admin')
    @commands.command(aliases=['erase'], brief='Erases one message by default.', hidden=True)
    async def clear(self, ctx, amount=1, pw=None):
        if amount > 5:

            if pw == 'begone':
                print('Correct password!')

            else:
                print(f'Password {pw} was wrong, capped at 5')
                amount = 5
                await self.post_log(f"🧹 ERASE: USER: `{ctx.message.author}` No password lol")

        # The +1 is because to erase the messages, the bot replies.
        await ctx.channel.purge(limit=amount+1)

        await self.post_log(f"🧹 ERASE: USER: `{ctx.message.author}` AMOUNT: `{amount}` LOCATION: `{ctx.message.channel.name}`")


def setup(client):
    client.add_cog(Basic(client))
