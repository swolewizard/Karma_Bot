import discord
import asyncio
from discord.ext import commands
import json
import datetime
import time
import re

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Replace 'channelidhere' with the ID of the desired channel
MONITORED_CHANNEL_ID = channelidhere

# Database to store karma points
DATABASE_FILE = "karma_db.json"

# Cooldown time in seconds
COOLDOWN_TIME = 300

# Add your bot token here
BOT_TOKEN = "bot token"


def load_database():
    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "userids" not in data or "cooldowns" not in data:
                # Migrate the old save format to the new one
                data = {"userids": data, "cooldowns": {}}
            return data
    except FileNotFoundError:
        return {"userids": {}, "cooldowns": {}}

def save_database(data):
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # Check if the message is from the monitored channel
    if message.channel.id != MONITORED_CHANNEL_ID:
        return

    if message.content.startswith("+karma"):
        # Check cooldown for this user
        author_id = str(message.author.id)
        current_time = int(time.time())

        if "cooldowns" not in bot_data:
            bot_data["cooldowns"] = {}

        if author_id in bot_data["cooldowns"]:
            last_time = bot_data["cooldowns"][author_id]
            if current_time - last_time < COOLDOWN_TIME:
                remaining_time = COOLDOWN_TIME - (current_time - last_time)
                await message.channel.send(f"**{message.author.name}**, you can use the +karma command again in {remaining_time} seconds.")
                return

        # Process the karma command
        args = message.content.split()
        if len(args) == 2 and args[0] == "+karma":
            user_mention = args[1]

            # Extract user ID from the mention using regular expression
            user_id_match = re.match(r"<@!?(\d+)>", user_mention)
            if not user_id_match:
                await message.channel.send(f"**{message.author.name}**, the user {user_mention} doesn't exist or is not a valid mention.")
                return

            user_id = int(user_id_match.group(1))
            mentioned_user = discord.utils.get(message.mentions, id=user_id)
            if not mentioned_user:
                await message.channel.send(f"**{message.author.name}**, the user {user_mention} doesn't exist or is not a valid mention.")
                return

            # Check if the mentioned user exists in the database
            if "userids" not in bot_data:
                bot_data["userids"] = {}

            if str(user_id) not in bot_data["userids"]:
                bot_data["userids"][str(user_id)] = 0

            bot_data["userids"][str(user_id)] += 1

            # Update the cooldown for this user
            bot_data["cooldowns"][author_id] = current_time

            # Save the updated data to the database
            save_database(bot_data)

            # Create the embed message
            embed = discord.Embed(
                description=f"<:karma:1134518591585259550> {mentioned_user.name}, {message.author.name} liked that.",
                color=0x00ff00  # You can change the color here (in this example, it's green).
            )

            # Check if the user should receive a role based on karma score
            karma_threshold_roles = {
                10: 1134524106243579935,
                20: 1134524156130639962,
                # Add more karma thresholds and role IDs here as needed
            }

            # Check if the user should receive a star based on karma score
            karma_threshold_stars = {
                10: 1134531554585092247
                # Add more karma thresholds and star role IDs here as needed
            }

            current_karma = bot_data["userids"].get(str(user_id), 0)

            # Give roles based on karma score
            for threshold, role_id in karma_threshold_roles.items():
                if current_karma >= threshold:
                    role = message.guild.get_role(role_id)
                    if role and role not in mentioned_user.roles:
                        try:
                            await mentioned_user.add_roles(role)
                            print(f"Gave {mentioned_user.name} role: {role.name}")
                        except discord.Forbidden:
                            print(f"Bot does not have permission to add role: {role.name}")
                    else:
                        print(f"Role not found or already assigned: {role_id}")

            # Give star roles based on karma score
            for threshold, star_role_id in karma_threshold_stars.items():
                if current_karma >= threshold:
                    star_role = message.guild.get_role(star_role_id)
                    if star_role and star_role not in mentioned_user.roles:
                        try:
                            await mentioned_user.add_roles(star_role)
                            print(f"Gave {mentioned_user.name} star role: {star_role.name}")
                        except discord.Forbidden:
                            print(f"Bot does not have permission to add star role: {star_role.name}")
                    else:
                        print(f"Star role not found or already assigned: {star_role_id}")

            user_role = None
            user_star = None
            # Find the highest role achieved by the user
            for threshold, role_id in reversed(list(karma_threshold_roles.items())):
                if current_karma >= threshold:
                    user_role = message.guild.get_role(role_id)
                    break
            # Find the highest role achieved by the user
            for threshold, star_role_id in reversed(list(karma_threshold_stars.items())):
                if current_karma >= threshold:
                    user_star = message.guild.get_role(star_role_id)
                    break

            # Add the field to the embed message
            if mentioned_user and user_role:
                embed.add_field(name=f"Current Karma: {current_karma}", value=f"{user_role.mention} {user_star.mention}", inline=False)
            elif mentioned_user:
                embed.add_field(name=f"Current Karma: {current_karma}", value="Trader tot —", inline=False)
            else:
                print("User not found")

            # Add the footer with the current time to the embed message
            current_time = datetime.datetime.now().strftime("%d/%m/%y, %I:%M %p")
            embed.set_footer(text=current_time)

            await message.channel.send(embed=embed)

        else:
            await message.channel.send(f"**{message.author.name}**, the karma command was used incorrectly. The correct usage is: +karma @username")

# Load the existing database
bot_data = load_database()

# Replace 'BOT_TOKEN' with your actual Discord bot token
client.run(BOT_TOKEN)
