import discord
from discord.ext import commands



class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener() #This is equal to @client.event, but for cogs.
    async def on_ready(self):
        print('FCC Bot is activated...')


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
    
    @commands.has_role('Admin')
    @commands.command(brief="Mess with what the bot is playing")
    async def activity(self, ctx, *, activity):
        print(f'Changed activity to "Playing {activity}"')
        await self.client.change_presence(activity=discord.Game(activity))

    
    @commands.command()
    async def role(cself, ctx, *, requested_role):

        #Acquire user
        user = ctx.message.author
        
        print(f'User {user} requests the role {requested_role}')

        # If they want help:
        if requested_role.lower() ==  'help':
            await ctx.send('Type .role FCC Ulsan or .role FCC Seoul to join the sub-group :)')
        else:

            possible_roles = ['FCC Ulsan', 'FCC Seoul']
            possible_roles_lower = [r.lower() for r in possible_roles]

            # Check to see if that role exists / is in the possible role list
            if requested_role.lower() in possible_roles_lower:
                print('User requests a valid role.')
                r_index = possible_roles_lower.index(requested_role.lower())
                possible_roles.pop(r_index)
            else:
                print('Role does not exist.')
                await ctx.send(f"Role {requested_role} isn't a possible role.")
                await ctx.send(f"Possible roles are: {(', ').join(possible_roles)}.")

            #Acquire existing roles to prevent double-roling :S
            user_existing_roles = [r.name.lower() for r in user.roles]
            
            # Admins can't have their roles edited
            if 'admin' in user_existing_roles:
                await ctx.send("Sorry: I am not permitted to alter an admin's roles.")

            else: #Not an admin

                if requested_role.lower() not in user_existing_roles:
                    #If the user isn't already that role already
                    # Add the role
                    await  user.add_roles(discord.utils.get(ctx.guild.roles, name=requested_role))
                    await ctx.send(f'{user} has joined the {requested_role} role.')

                    # Check for opposite role:
                    for role_removal in possible_roles:
                        await user.remove_roles(discord.utils.get(ctx.guild.roles, name=role_removal))
                        await ctx.send(f'You were removed from the {role_removal} role.')


                else:
                    await ctx.send(f'You already have that role')

        
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