import discord
from discord.ext import commands


emoji_roles = {
    "🇰🇷": "Seoul-based",
    "🏙️": "Ulsan-based",
    "🌉": "Busan-based",
    "🛫": "Overseas-based",
}

location_based_roles = emoji_roles.values()

NOLOCATIONROLE = "No-location"


class Roles(commands.Cog):

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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if user responds to BOT ONLY in REACT-FOR-ROLES only
        if reaction.message.channel.name == "react-for-roles" and reaction.message.author.bot == True:

            user_existing_roles = [role.name for role in user.roles]
            # Can't edit admin roles!
            if "Admin" not in user_existing_roles:

                try:

                    # Respond only to correct emoji
                    if reaction.emoji in emoji_roles.keys():

                        requested_role = emoji_roles[reaction.emoji]
                        if requested_role not in user_existing_roles:
                            await user.add_roles(discord.utils.get(user.guild.roles, name=requested_role))
                            print(
                                f"Role {requested_role} added to {user.name}")
                            await self.post_log(f"🏷️ REACT-ROLE: ADD ROLE: USER:{user}: gains {requested_role} => {user_existing_roles}")

                        if NOLOCATIONROLE in user_existing_roles:
                            await user.remove_roles(discord.utils.get(user.guild.roles, name=NOLOCATIONROLE))
                            print(
                                f"Role {NOLOCATIONROLE} removed from {user.name}")
                            await self.post_log(f"🏷️ REACT-ROLE: ADD ROLE: USER:{user}: is no longer {NOLOCATIONROLE}")

                    else:
                        await self.post_log(f"REACT-ROLE: USER {user} used {reaction.emoji}, but it failed")

                except Exception as error:
                    await self.post_log(f"🚨 REACT-ROLE: ADDING ROLE: USER:{user}: {user_existing_roles}")
                    await self.post_log(f"```python {error}```")
                    raise(error)
            else:
                await self.post_log(f"🧻 ROLE: Admin {user} can't change roles")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.channel.name == "react-for-roles" and reaction.message.author.bot == True:

            user_existing_roles = [role.name for role in user.roles]
            # Can't edit admin roles!
            if "Admin" not in user_existing_roles:

                try:
                    user_existing_roles = [role.name for role in user.roles]

                    # Respond only to correct emoji
                    if reaction.emoji in emoji_roles.keys():

                        requested_role = emoji_roles[reaction.emoji]

                        if requested_role in user_existing_roles:
                            await user.remove_roles(discord.utils.get(user.guild.roles, name=requested_role))
                            user_existing_roles.remove(requested_role)
                            print(
                                f"Role {requested_role} removed from {user.name}")
                            await self.post_log(f"🏷️ REACT-ROLE: REMOVING ROLE: USER:{user}: Removes {requested_role} => {user_existing_roles}")

                            # check roles a user has
                            # if none of the location roles are in their thing, set them to no-location

                            should_assign_no_location = True
                            for role in location_based_roles:
                                if role in user_existing_roles:
                                    should_assign_no_location = False
                                    await self.post_log(f"🏷️ REACT-ROLE: USER:{user}: will NOT become {NOLOCATIONROLE}")
                                    break

                            if should_assign_no_location:
                                await user.add_roles(discord.utils.get(user.guild.roles, name=NOLOCATIONROLE))
                                await self.post_log(f"🏷️ REACT-ROLE: USER:{user}: Becomes {NOLOCATIONROLE}")

                except Exception as error:
                    await self.post_log(f"🚨 REACT-ROLE: REMOVING ROLE: USER:{user}: {user_existing_roles}")
                    await self.post_log(f"```python {error}```")
                    raise(error)

            else:
                await self.post_log(f"🧻 ROLE: Admin {user} can't change roles")


def setup(client):
    client.add_cog(Roles(client))
