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
SPECIFIED_CHANNEL_NAME = os.getenv('SPECIFIED_CHANNEL_NAME')
SHOT_RECIPIENT_ID = int(os.getenv("SHOT_RECIPIENT_ID"))

logger.debug("DISCORD_TOKEN: {0}".format(DISCORD_TOKEN))
logger.debug("GUILD_NAME: {0}".format(GUILD_NAME))
logger.debug("SPECIFIED_CHANNEL_NAME: {0}".format(SPECIFIED_CHANNEL_NAME))
logger.debug("SHOT_RECIPIENT_ID: {0}".format(SHOT_RECIPIENT_ID))
#logger.debug("type(SHOT_RECIPIENT_ID) = {0}".format(type(SHOT_RECIPIENT_ID))

command_prefix = "$"

command_list = {
    "help":     "help",
    "about":    "why",
    "pour":     "pour",
    "fill":     "punish"
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
    print(dir(client))
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
        
    is_pour_command = (message.content == await getCommandFor("pour"))
    is_fill_command = (message.content == await getCommandFor("fill"))
        
    if message.content == await getCommandFor("about"):
        logger.info("{0.author} asked why the hell this even exsits".format(message))
        await message.channel.send("Fuck you, that's why <3\nBuilt with love and too much time")
        
    
    elif (is_pour_command or is_fill_command):
        logger.debug("Pouring command registered")
        
        if (is_pour_command and not command_timer.isSingleTimerReady()) or (is_fill_command and not command_timer.isFillTimerReady()):
            single_timer_remaining, fill_timer_remaining = command_timer.getTimerTimeRemaining()
            single_remaining_str_min = str(int(single_timer_remaining))
            single_remaining_str_sec = "{:02d}".format(int(round((single_timer_remaining-int(single_timer_remaining))*60)))
            single_remaining_str = single_remaining_str_min + ":" single_remaining_str_sec
            fill_remaining_str_min = str(int(fill_timer_remaining))
            fill_remaining_str_sec = "{:02d}".format(int(round((fill_timer_remaining-int(fill_timer_remaining))*60)))
            fill_remaining_str = fill_remaining_str_min + ":" fill_remaining_str_sec
            logger.info("Damn, {0.author} really wanted to make {1} drink, but the timer isn't up!".format(message, await getShotRecipient()))
            logger.info("Time remaining for single pour: {0}".format(single_remaining_str))
            logger.info("Time remaining for full pour: {0}".format(fill_remaining_str))
            choose_time_remaining = single_remaining_str if is_pour_command else fill_remaining_str
            await message.channel.send("Woah, woah, woah - slow down there, {0.author}!  {1} still has about {2} left before you can do that!".format(message, await getShotRecipient(), choose_time_remaining))
            return
            
        if command_timer.isInProgress():
            logger.info("Haha, {0.author} wanted to pour {1} a shit, but ShotBot is still working on the last command".format(message, await getShotRecipient()))
            await message.channel.send("Slow down there, {0.author} - I'm still working on pouring the last drink for {1}!".format(message, await getShotRecipient()))
            
        if command_timer.isUserLockSet():
            logger.info("User lockout is set, will not pour shot(s)")
            await message.channel.send("Sorry, {0.author}!  Looks like {1} isn't ready for another one yet!".format(message, await getShotRecipient()))
            return
            
        command_timer.setInProgress()
        
        if is_pour_command:
            logger.info("{0.author} attempted to pour {1} shot".format(message, await getShotRecipient()))
            command_timer.resetTimers()
            # pour a shot glass
            
        else:
            logger.info("{0.author} attempted to punish {1}, what a jerk".format(message, await getShotRecipient()))
            # pour all glasses
            
        command_timer.markProgressComplete()
        command_timer.resetTimers()
        
    elif message.content == await getCommandFor("help"):
        logger.info("{0.author} asked for help".format(message))
        help_message = ""
        help_dict = await getCommandHelp()
        print(help_dict)
        for command, help_text in help_dict.items():
            help_message += "".join([command, ": ", help_text, "\n"])
        help_message += "".join(["\n", "Created by Tekktrik using Python"])
        await message.channel.send(help_message)
        
    elif message.content.startswith(command_prefix):
        logger.info("{0.author} seemingly tried to use an invalid command".format(message))
        await message.channel.send("Beep boop, does not compute.  Try using $help command.")
    
    return
        
client.run(DISCORD_TOKEN)