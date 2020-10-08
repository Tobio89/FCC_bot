import discord
from discord.ext import commands
from datetime import datetime


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener() #This is equal to @client.event, but for cogs.
    async def on_ready(self):
        print('FCC Bot is activated...')
    

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'User {member} has joined.')
        server = member.guild
        general_channel = discord.utils.get(server.text_channels, name="general")
        newcomer_role = discord.utils.get(server.roles, name="Newcomers")
        await member.add_roles(newcomer_role)
        await general_channel.send(f"Welcome, @{member}! Please tell us which FCC group you're from! Type !role FCC Seoul or !role FCC Ulsan to join that group right here on the FCC Korea discord!")



    # Commands
    @commands.command(brief='Find out your latency!') #This allows you to do commands.
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
        
        #The +1 is because to erase the messages, the bot replies.
        await ctx.channel.purge(limit=amount+1)


    @commands.has_role('Admin')
    @commands.command(brief='Change the bot status', hidden=True)
    async def status(self, ctx, status):
        statuses = {
            'idle' : discord.Status.idle,
            'online' : discord.Status.online,
            'offline': discord.Status.offline,
            'dnd': discord.Status.do_not_disturb,
            'invisible': discord.Status.invisible
        }
        print(f'Changed status to {status}')
        if status == 'help':
            await ctx.send('Status can be: online, idle, dnd, invisible and offline.')
                
        try:
            await self.client.change_presence(status=statuses[status]) # This line is about statuses
        except:
            await ctx.send(f"Nope, I'm not being {status}. Try online, idle, dnd, invisible or offline")
    

    @commands.command()
    async def role(cself, ctx, *, requested_role):

        #Acquire user
        user = ctx.message.author
        
        print(f'User {user} requests the role {requested_role}')

        # If they want help:
        if requested_role.lower() ==  'help':
            await ctx.send('Type .role FCC Ulsan or .role FCC Seoul to join the sub-group :)')


        # If they actually entered a role:
        else:

            #Acquire existing roles to prevent double-roling
            user_existing_roles = [r.name.lower() for r in user.roles]

            # Admins can't have their roles edited
            if 'admin' in user_existing_roles:
                await ctx.send("Sorry: I am not permitted to alter an admin's roles.")

            # Handle requesting a role they're already in
            elif requested_role.lower() in user_existing_roles:
                await ctx.send("It looks like you're already in that group. You can't join twice!")
            
            # Not an admin:
            else:

                possible_roles = ['FCC Ulsan', 'FCC Seoul']
                possible_roles_lower = [r.lower() for r in possible_roles]

                # The role is a valid role they can join
                if requested_role.lower() in possible_roles_lower:
                    print(f'User requests valid role: {requested_role}')

                    # Remove the user from the Newcomers group.
                    if 'newcomers' in user_existing_roles:
                        await user.remove_roles(discord.utils.get(ctx.guild.roles, name='Newcomers'))
                        
                        await ctx.send(f'Thanks for joining a group!\nYou were removed from the Newcomers group')

                    
                    for role in possible_roles:
                        # If the user is already in a group:
                        if role.lower() in user_existing_roles:
                            await user.remove_roles(discord.utils.get(ctx.guild.roles, name=role))
                            await ctx.send(f'You are no longer in the {role} group.')
                            print(f'User was removed from {role}')
                    

                    await user.add_roles(discord.utils.get(ctx.guild.roles, name=requested_role))
                    await ctx.send(f'You are now in the {requested_role} group.')
                
                #The role they entered isn't possible (doesn't exist or no permission)
                else:
                    await ctx.send(f"You can't join the {requested_role} group.")


        
    @commands.command()
    async def voice(cself, ctx):

        user = ctx.message.author
        user_existing_roles = [r.name.lower() for r in user.roles]

        print(f'{user} requests altering voice capabilities')

        if 'voice_chat' not in user_existing_roles:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name='voice_chat'))
            await ctx.send(f'{user}: voice chatting capabilities ARMED')

        else:
            
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name='voice_chat'))
            await ctx.send(f'{user}: voice chatting capabilities DISARMED.')

            voice_channel = discord.utils.get(ctx.guild.channels, name='VOICE CHAT', type=discord.ChannelType.voice)
            members_in_voice_channel = voice_channel.members

            if user in members_in_voice_channel:
                print(f'{user} is present in the voice channel - kicking')

                kick_channel = await ctx.guild.create_voice_channel("kick")
                await user.move_to(kick_channel, reason="You requested to deactivate voice capabilities")
                await kick_channel.delete()
                
 

def setup(client):
    client.add_cog(Basic(client))