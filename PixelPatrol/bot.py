
##############################################################################################################################################
# ________       ___    ___ ________  ________  ________  _________        ________  _________  ________  _________  ___  ___  ________      #
#|\   ____\     |\  \  /  /|\   ____\|\   __  \|\   __  \|\___   ___\     |\   ____\|\___   ___\\   __  \|\___   ___\\  \|\  \|\   ____\     # 
#\ \  \___|_    \ \  \/  / | \  \___|\ \  \|\ /\ \  \|\  \|___ \  \_|     \ \  \___|\|___ \  \_\ \  \|\  \|___ \  \_\ \  \\\  \ \  \___|_    #
# \ \_____  \    \ \    / / \ \_____  \ \   __  \ \  \\\  \   \ \  \       \ \_____  \   \ \  \ \ \   __  \   \ \  \ \ \  \\\  \ \_____  \   #
#  \|____|\  \    \/  /  /   \|____|\  \ \  \|\  \ \  \\\  \   \ \  \       \|____|\  \   \ \  \ \ \  \ \  \   \ \  \ \ \  \\\  \|____|\  \  #
#    ____\_\  \ __/  / /       ____\_\  \ \_______\ \_______\   \ \__\        ____\_\  \   \ \__\ \ \__\ \__\   \ \__\ \ \_______\____\_\  \ #
#   |\_________\\___/ /       |\_________\|_______|\|_______|    \|__|       |\_________\   \|__|  \|__|\|__|    \|__|  \|_______|\_________\#
#   \|_________\|___|/        \|_________|                                   \|_________|                                        \|_________|#
##############################################################################################################################################                                                                                                                                            
                                                                                                                                          

import discord
import json
import re
from discord.ext import commands, tasks
import time
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.guild_messages = True
intents.message_content = True
intents.reactions = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables to keep track of last message times, offline notifications, and last known status
last_message_times = {}
guild_channels = {}
sent_offline_notifications = {}
last_known_status = {}
has_started = False

# Load/Save channels to JSON
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_from_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}



@bot.event
async def on_ready():
    global guild_channels, last_known_status, last_message_times, initial_run, has_started

    if has_started:
        return
    
    print(f"We have logged in as {bot.user}")
    guild_channels = load_from_json("./PixelPatrol/guild_channels.json")
    last_known_status = load_from_json("./PixelPatrol/last_known_status.json")

    for channel_id, status in last_known_status.items():
        if status == "online":
            last_message_times[channel_id] = time.time()

    initial_run = True  # Reset the flag so that check_for_inactivity knows to skip its first run
    has_started = True

# Log channel setup
@bot.command()
async def logchannel(ctx, log_channel: discord.TextChannel, update_channel: discord.TextChannel):
    global guild_channels
    guild_id = str(ctx.guild.id)
    if guild_id not in guild_channels:
        guild_channels[guild_id] = {}

    if str(log_channel.id) in guild_channels[guild_id]:
        await ctx.send(f"{log_channel.mention} is already being monitored. To update, please remove it first.")
        return

    guild_channels[guild_id][str(log_channel.id)] = str(update_channel.id)
    save_to_json(guild_channels, "./PixelPatrol/guild_channels.json")
    await ctx.send(f"Monitoring {log_channel.mention}. Updates will be sent to {update_channel.mention}")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    guild_id = str(message.guild.id)
    channel_id = str(message.channel.id)

    # Check if it's a bot message and if the channel is either a logging or update channel.
    if message.author.bot and guild_id in guild_channels and (channel_id in guild_channels[guild_id].keys() or channel_id in guild_channels[guild_id].values()):
        #print(f"[DEBUG] Message received in guild {message.guild.id} from channel {message.channel.id} by {message.author.name}: {message.content[:50]}...")  # Moved inside the conditional check
        if channel_id in guild_channels[guild_id]:
            log_channel_id = channel_id
            update_channel_id = guild_channels[guild_id][channel_id]
        else:
            # The channel_id must be an update channel. We need to find the associated logging channel.
            log_channel_id = [key for key, value in guild_channels[guild_id].items() if value == channel_id][0]
            update_channel_id = channel_id

        update_channel = bot.get_channel(int(update_channel_id))
        current_status = "unknown"  # Fallback status

        if re.search(r'\bdisconnected\b', message.content, re.IGNORECASE) or re.search(r'cancellationtoken', message.content, re.IGNORECASE) or re.search(r'detaching controllers', message.content, re.IGNORECASE):
            if last_known_status.get(channel_id) != "offline":
                # Update the last_known_status to offline and save to JSON
                last_known_status[log_channel_id] = "offline"
                save_to_json(last_known_status, "./PixelPatrol/last_known_status.json")
                # Send Offline Embed
                embed = discord.Embed(title="Status Update - Offline!", description="I have detected that this bot is having issues and is not connected and working.", color=0xff0000)
                embed.set_image(url="attachment://offline.gif")  # Set the offline GIF image
                current_status = "offline"
                await update_channel.send(embed=embed, file=discord.File("./PixelPatrol/offline.gif"))
                new_name = f"❌{update_channel.name.replace('❌', '').replace('✅', '')}"
                await update_channel.edit(name=new_name)
            

        elif re.search(r'\bidentified as\b', message.content, re.IGNORECASE) or re.search(r'added logging to discord channel', message.content, re.IGNORECASE) or re.search(r'dump:', message.content, re.IGNORECASE):
            if last_known_status.get(channel_id) != "online":
                # Update the last_known_status to online and save to JSON
                last_known_status[channel_id] = "online"
                save_to_json(last_known_status, "./PixelPatrol/last_known_status.json")
                # Send Online Status Embed
                embed = discord.Embed(title="Status Update - Online!", description="I have detected that this bot is online and in working order.", color=0x00ff00)
                embed.set_image(url="attachment://online.gif")  # Set the online GIF image
                current_status = "online"
                await update_channel.send(embed=embed, file=discord.File("./PixelPatrol/online.gif"))
                new_name = f"✅{update_channel.name.replace('❌', '').replace('✅', '')}"
                await update_channel.edit(name=new_name)
                


        # Update last_known_status and save to JSON only when status changes from "online" to "offline" or vice versa
        if current_status != "unknown" and (channel_id not in last_known_status or last_known_status[channel_id] != current_status):
            last_known_status[channel_id] = current_status
            save_to_json(last_known_status, "./PixelPatrol/last_known_status.json")

        last_message_times[channel_id] = time.time()

        if re.search(r'\btrade\b|\bt\b', message.content, re.IGNORECASE):
            log_channel_id = None
            for potential_log_channel_id, update_channel_id in guild_channels[guild_id].items():
                if str(update_channel_id) == channel_id:
                    log_channel_id = potential_log_channel_id
                    break

            if log_channel_id:
                try:
                    def check_response(m):
                        # Ensure that the message is from the bot and in the correct channel
                        return m.channel.id == int(log_channel_id) and m.author.bot

                    response_message = await bot.wait_for('message', check=check_response, timeout=30)  # wait for 30 seconds

                    # If bot replies with "Oops!", it means the trade didn't go through
                    if "wasn't able to create" in response_message.content:
                        return

                except asyncio.TimeoutError:
                    # Default to online if channel status is not known.
                    if log_channel_id not in last_known_status:
                        last_known_status[log_channel_id] = "online"

                    # Send offline notification only if last_known_status is online
                    if last_known_status.get(log_channel_id) == "offline":
                        embed = discord.Embed(title="Status Update - Offline!", description="I have detected that this bot is having issues and is not connected and working.", color=0xff0000)
                        embed.set_image(url="attachment://offline.gif")
                        await update_channel.send(embed=embed, file=discord.File("./PixelPatrol/offline.gif"))
                        new_name = f"❌{update_channel.name.replace('❌', '').replace('✅', '')}"
                        await update_channel.edit(name=new_name)

                        # Update the last_known_status to offline and save to JSON
                        last_known_status[log_channel_id] = "offline"
                        save_to_json(last_known_status, "./PixelPatrol/last_known_status.json")


@bot.command(name="online")
@commands.has_permissions(manage_messages=True)  # Optional: Only allows users with "Manage Messages" permission to use the command
async def mark_online(ctx):
    global last_known_status
    channel_id = str(ctx.channel.id)
    last_known_status[channel_id] = "online"
    save_to_json(last_known_status, "./PixelPatrol/last_known_status.json")
    
    embed = discord.Embed(title="Status Update - Online!", description="I have detected that this bot is online and in working order.", color=0x00ff00)
    embed.set_image(url="attachment://online.gif")
    await ctx.send(embed=embed, file=discord.File("./PixelPatrol/online.gif"))
    
    new_name = f"✅{ctx.channel.name.replace('❌', '').replace('✅', '')}"
    await ctx.channel.edit(name=new_name)
    
    # Delete the user's command
    await ctx.message.delete()


@bot.command(name="offline")
@commands.has_permissions(manage_messages=True)  # Optional: Only allows users with "Manage Messages" permission to use the command
async def mark_offline(ctx):
    global last_known_status
    channel_id = str(ctx.channel.id)
    last_known_status[channel_id] = "offline"
    save_to_json(last_known_status, "./PixelPatrol/last_known_status.json")
    
    embed = discord.Embed(title="Status Update - Offline!", description="I have detected that this bot is having issues and is not connected and working.", color=0xff0000)
    embed.set_image(url="attachment://offline.gif")
    await ctx.send(embed=embed, file=discord.File("./PixelPatrol/offline.gif"))
    
    new_name = f"❌{ctx.channel.name.replace('❌', '').replace('✅', '')}"
    await ctx.channel.edit(name=new_name)
    
    # Delete the user's command
    await ctx.message.delete()


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Simply ignore and return if the command is not found.
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument(s). Please provide both the log channel and the update channel.")
    else:
        await ctx.send(f"An unknown error occurred: {error}")


# Replace TOKEN with your actual bot token
bot.run('MTE0NTEyNDgzMjQ5NzkwNTcyNA.GZsiSz.f9yKSFcydfMdmS30-7zZnfkky8WUEsCQ5LuxSI')
