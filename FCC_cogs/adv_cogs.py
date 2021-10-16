import discord
from discord.ext import commands


class Advanced(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.server = None
        self.log_channel = None

    async def post_log(self, message: str):
        if (self.server and self.log_channel):
            await self.log_channel.send(message)

    @commands.Cog.listener()  # This is equal to @client.event, but for cogs.
    async def on_ready(self):
        self.server = discord.utils.get(self.client.guilds)
        self.log_channel = discord.utils.get(
            self.server.text_channels, name="bot-logs")

    @commands.command(brief='Quickly search Stack Overflow')
    async def stack(self, ctx, *, search_terms):
        terms = '+'.join(search_terms.split())

        SO_URL = "https://stackoverflow.com/search?q="

        await ctx.send(f'{SO_URL}{terms}')
        await self.post_log(f"🔎 SEARCH: USER: {ctx.message.author} TERMS: {terms}")


def setup(client):
    client.add_cog(Advanced(client))
