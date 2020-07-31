import discord
from discord.ext import commands



class Advanced(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Quickly search Stack Overflow')
    async def stack(self, ctx, *, search_terms):
        terms = '+'.join(search_terms.split())

        SO_URL = "https://stackoverflow.com/search?q="

        await ctx.send(f'{SO_URL}{terms}')

 

def setup(client):
    client.add_cog(Advanced(client))