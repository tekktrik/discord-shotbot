import discord
import logging
import os
import time
import asyncio
from dotenv import load_dotenv
from CommandTimer import CommandTimer

client = discord.Client()
logger = logging.getLogger('shotbot_client')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='shotbot_client.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
logger.debug("Used load_dotenv() to load environment")

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = os.getenv('GUILD_NAME')
GUILD_ID = os.getenv('GUILD_ID')
SPECIFIED_CHANNEL_NAME = os.getenv('SPECIFIED_CHANNEL_NAME')
SHOT_RECIPIENT_ID = int(os.getenv("SHOT_RECIPIENT_ID"))

logger.debug("DISCORD_TOKEN: {0}".format(DISCORD_TOKEN))
logger.debug("GUILD_NAME: {0}".format(GUILD_NAME))
logger.debug("GUILD_ID: {0}".format(GUILD_ID))
logger.debug("SPECIFIED_CHANNEL_NAME: {0}".format(SPECIFIED_CHANNEL_NAME))
logger.debug("SHOT_RECIPIENT_ID: {0}".format(SHOT_RECIPIENT_ID))

command_prefix = "$"

command_list = {
    "help":     "help",
    "about":    "why",
    "pour":     "pour",
    "fill":     "punish",
    "shutdown": "mercy"
}

command_timer = CommandTimer()

async def getShotRecipient():
    return await client.fetch_user(SHOT_RECIPIENT_ID)

async def getCommandFor(input_string):
    return command_prefix+command_list[input_string]

async def getCommandHelp():
    return {
        await getCommandFor("help"): "Display help regarding Discord-ShotBot (That's this)",
        await getCommandFor("about"): "Why was an abomination like me created?",
        await getCommandFor("pour"): "Pour {0.name} a glass".format(await getShotRecipient()),
        await getCommandFor("fill"): "{0.name} won't learn otherwise".format(await getShotRecipient())
    }

@client.event
async def on_ready():
    logger.info("Logging in successfully as {0.user}, ready to go!".format(client))
    for guild in client.guilds:
        if guild.name == GUILD_NAME:
            for channel in guild.channels:
                if channel.name == SPECIFIED_CHANNEL_NAME:
                    await channel.send("Hello, humans!  I am Discord-ShotBot², and I am here to ruin {0.name}'s day!".format(await getShotRecipient()))
                    break
            break

@bot.slash_command(guild_id=GUILD_ID)
async def pour(ctx):
    """Pour a shot for the recipient"""
    logger.debug("Slash command for pour registered")
    await ctx.send("Now pouring a shot!")
        
client.run(DISCORD_TOKEN)