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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if user responds to BOT ONLY in REACT-FOR-ROLES only
        if reaction.message.channel.name == "react-for-roles" and reaction.message.author.bot == True:

            user_existing_roles = [role.name for role in user.roles]
            # Can't edit admin roles!
            if "Admin" not in user_existing_roles:

                print(user_existing_roles)
                print(location_based_roles)

                # Respond only to correct emoji
                if reaction.emoji in emoji_roles.keys():

                    requested_role = emoji_roles[reaction.emoji]
                    print(user_existing_roles)
                    print("Role to add: ", emoji_roles[reaction.emoji])
                    if requested_role not in user_existing_roles:
                        await user.add_roles(discord.utils.get(user.guild.roles, name=requested_role))
                        print(f"Role {requested_role} added to {user.name}")

                    if NOLOCATIONROLE in user_existing_roles:
                        await user.remove_roles(discord.utils.get(user.guild.roles, name=NOLOCATIONROLE))
                        print(
                            f"Role {NOLOCATIONROLE} removed from {user.name}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.channel.name == "react-for-roles" and reaction.message.author.bot == True:

            user_existing_roles = [role.name for role in user.roles]
            # Can't edit admin roles!
            if "Admin" not in user_existing_roles:

                user_existing_roles = [role.name for role in user.roles]

                # Respond only to correct emoji
                if reaction.emoji in emoji_roles.keys():

                    requested_role = emoji_roles[reaction.emoji]

                    print("Role to remove: ", emoji_roles[reaction.emoji])

                    if requested_role in user_existing_roles:
                        await user.remove_roles(discord.utils.get(user.guild.roles, name=requested_role))
                        user_existing_roles.remove(requested_role)
                        print(
                            f"Role {requested_role} removed from {user.name}")

                        # check roles a user has
                        # if none of the location roles are in their thing, set them to no-location

                        should_assign_no_location = True
                        for role in location_based_roles:
                            if role in user_existing_roles:
                                should_assign_no_location = False
                                break

                        if should_assign_no_location:
                            await user.add_roles(discord.utils.get(user.guild.roles, name=NOLOCATIONROLE))


def setup(client):
    client.add_cog(Roles(client))
