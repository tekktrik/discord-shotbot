import discord
import logging
import os
from dotenv import load_dotenv

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
SPECIFIED_CHANNEL_NAME = os.getenv('SPECIFIED_CHANNEL_NAME')

command_prefix = "$"

def getCommandFor(input_string):
    return command_prefix+input_string

command_list = {
    "help": "help",
    "about": "why",
    "pour": "pour",
    "fill": "punish"
}

command_help = {
    getCommandFor(command_list["help"]: "Display help regarding Discord-ShotBot",
    getCommandFor(command_list["about"]: "Why was an abomination like me created?",
    getCommandFor(command_list["pour"]: "Pour Tekktrik a glass",
    getCommandFor(command_list["fill"]: "He won't learn otherwise"
}

command_help

class CommandTimer:

    def __init__(self, id_string):
    
        self._id = id_string
        self._unlock_command = time.time()

@client.event
async def on_ready():
    logger.info("Logging in successfully as {0.user}, ready to go!".format(client))
    # send message that bot is ready
    
@client.event
async def on_message(message):
    # Ignore bot's own messages
    if message.author == client.user:
        return
        
    # Only work with messages from the specified server
    if message.guild.name != GUILD_NAME:
        logger.debug("Logged message from {0.author} from server \"{0.guild.name}\" ({0.guild.id}): {0.content}".format(message))
        return
    
    # Ignore message from non-specified channels
    if message.channel.name != SPECIFIED_CHANNEL_NAME:
        return
        
    if message.content == getCommandFor("about"):
        logger.info("{0.author} asked why the hell this even exsits".format(message))
        await message.channel.send(
            "Fuck you, that's why <3\n\
            Built with love and too much time"
        )
        
    elif message.content == getCommandFor("pour"):
        logger.info("{0.author} attempted to pour {1.user} shot".format(message, client))
        # pour a shot glass
        
    elif message.content == getCommandFor("fill"):
        logger.info("{0.author} attempted to punish {1.user}, what a jerk".format(message, client))
        # pour all glasses
        
    elif message.content.startswith(command_prefix):
        await message.channel.send("Beep boop, does not compute.  Try using $help command.")
        logger.info("{0.author} seemingly tried to use an invalid command".format(message))
        
client.run(DISCORD_TOKEN)